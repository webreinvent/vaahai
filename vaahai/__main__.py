"""
Main entry point for the Vaahai CLI application.

This module initializes the Typer application and registers all commands.
It uses a plugin architecture to dynamically load commands and handle dependencies.
"""

import typer
from rich.console import Console
from typing import Optional, List, Dict, Any, Callable
import sys
from pathlib import Path
import os
import subprocess
import importlib.util
import platform
import ctypes.util
from functools import lru_cache

from vaahai import __version__

# Create console for rich output
console = Console()

# Initialize the CLI app
app = typer.Typer(
    help="Vaahai CLI tool for AI-assisted development",
    no_args_is_help=True,
    add_completion=False,
)

def find_standalone_script() -> Optional[str]:
    """Find the standalone detect-language script in various possible locations."""
    possible_locations = [
        # Local development environment
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", "vaahai-detect-language-script"),
        # System-wide installation
        "/usr/local/bin/vaahai-detect-language-script",
        # User local installation
        os.path.expanduser("~/.local/bin/vaahai-detect-language-script"),
        # Project local installation
        os.path.join(os.getcwd(), "local", "bin", "vaahai-detect-language-script"),
        # Current directory (for testing)
        os.path.join(os.getcwd(), "vaahai-detect-language-script"),
        # Installed via pip
        os.path.join(os.path.dirname(sys.executable), "vaahai-detect-language-script"),
    ]
    
    for location in possible_locations:
        if os.path.isfile(location) and os.access(location, os.X_OK):
            return location
    
    return None

def handle_detect_language_command() -> int:
    """Handle the detect-language command by delegating to the standalone script."""
    try:
        # Find the standalone script
        script_path = find_standalone_script()
        
        if not script_path:
            console.print("[bold red]Error: Standalone detect-language script not found.[/bold red]")
            console.print("[bold yellow]To install the standalone script, run:[/bold yellow]")
            print("  pip install vaahai[ml]")
            console.print("[bold yellow]Or install it locally with:[/bold yellow]")
            print("  ./bin/install-detect-language.sh --local")
            print("  export PATH=\"$PWD/local/bin:$PATH\"")
            return 1
        
        # Build command arguments
        cmd = [script_path]
        
        # Add all arguments after "detect-language"
        # Skip the first two arguments (script name and "detect-language")
        if len(sys.argv) > 2:
            cmd.extend(sys.argv[2:])
        
        # Run the standalone script
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode
    except Exception as e:
        debug = "--debug" in sys.argv
        if debug:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            console.print("[bold red]Traceback:[/bold red]")
            import traceback
            console.print(traceback.format_exc())
        else:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            console.print("[bold yellow]Run with --debug for more information.[/bold yellow]")
        return 1

def main():
    """Main entry point for the CLI."""
    # Use Typer to handle all commands
    try:
        return app()
    except Exception as e:
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        else:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return 1

# Define command groups
CORE_COMMANDS = ["config"]
ML_COMMANDS = ["review", "analyze", "explain", "document", "helloworld", "detect_language"]

# Track which commands have been registered
registered_commands = set()

def version_callback(value: bool):
    """Print the version and exit."""
    if value:
        console.print(f"[bold]Vaahai[/bold] version: [bold green]{__version__}[/bold green]")
        sys.exit(0)
    return value

@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True, help="Show version and exit."
    ),
):
    """
    Vaahai: AI-augmented code review CLI tool.
    
    Combines static analysis with LLM capabilities to provide comprehensive
    code reviews, suggestions, and automated fixes.
    """
    pass

#
# Dependency checking utilities
#

def is_module_available(module_name: str) -> bool:
    """Check if a Python module is available without importing it."""
    return importlib.util.find_spec(module_name) is not None

def is_library_available(lib_name: str) -> bool:
    """Check if a system library is available."""
    return ctypes.util.find_library(lib_name) is not None

@lru_cache(maxsize=1)
def check_xgboost_with_openmp() -> bool:
    """
    Check if XGBoost is available with OpenMP support without importing it.
    This is particularly important for macOS where OpenMP is not installed by default.
    """
    # First check if XGBoost is installed
    if not is_module_available("xgboost"):
        return False
    
    # On macOS, check if OpenMP is available
    if platform.system() == "Darwin":
        # Check for libomp
        if not is_library_available("omp"):
            return False
    
    # On other platforms, assume XGBoost works with OpenMP
    return True

def get_missing_ml_dependencies() -> List[str]:
    """Get a list of missing ML dependencies."""
    missing = []
    
    if not is_module_available("openai"):
        missing.append("openai")
    
    if not is_module_available("pyautogen"):
        missing.append("pyautogen")
    
    if not is_module_available("flaml"):
        missing.append("flaml")
    
    if not check_xgboost_with_openmp():
        missing.append("xgboost+openmp")
    
    return missing

def can_load_ml_commands() -> bool:
    """Check if all ML dependencies are available."""
    return len(get_missing_ml_dependencies()) == 0

#
# Command registration
#

def register_core_commands() -> None:
    """Register core commands that don't depend on ML libraries."""
    for cmd_name in CORE_COMMANDS:
        try:
            # Import the command module
            module_name = f"vaahai.cli.commands.{cmd_name}"
            module = importlib.import_module(module_name)
            
            # Register the command with the app
            if hasattr(module, "register"):
                module.register(app)
                registered_commands.add(cmd_name)
        except ImportError as e:
            console.print(f"[bold red]Error loading core command '{cmd_name}':[/bold red] {str(e)}")

def register_ml_commands() -> Dict[str, bool]:
    """Register commands that depend on ML libraries."""
    results = {}
    
    # First try to register detect_language command separately
    if "detect_language" in ML_COMMANDS:
        try:
            module_name = "vaahai.cli.commands.detect_language"
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register(app)
                registered_commands.add("detect_language")
                results["detect_language"] = True
            else:
                results["detect_language"] = False
        except ImportError as e:
            results["detect_language"] = False
    
    # Register other ML commands if dependencies are available
    if can_load_ml_commands():
        for cmd_name in [cmd for cmd in ML_COMMANDS if cmd != "detect_language"]:
            try:
                # Import the command module
                module_name = f"vaahai.cli.commands.{cmd_name}"
                module = importlib.import_module(module_name)
                
                # Register the command with the app
                if hasattr(module, "register"):
                    module.register(app)
                    registered_commands.add(cmd_name)
                    results[cmd_name] = True
                else:
                    results[cmd_name] = False
            except ImportError as e:
                # Don't show error here - we'll handle it in the stub commands
                results[cmd_name] = False
    else:
        # Mark other commands as not registered
        for cmd_name in [cmd for cmd in ML_COMMANDS if cmd != "detect_language"]:
            results[cmd_name] = False
    
    return results

def register_stub_commands() -> None:
    """Register stub commands for ML-dependent commands that couldn't be registered."""
    for cmd_name in ML_COMMANDS:
        if cmd_name not in registered_commands:
            # Create a stub command function with the correct name
            def create_stub_command(name: str) -> Callable:
                def stub_command():
                    """This command requires ML dependencies."""
                    # Show a helpful error message
                    console.print(f"[bold red]Error:[/bold red] The '{name}' command requires additional dependencies.")
                    
                    # Get missing dependencies
                    missing = get_missing_ml_dependencies()
                    
                    if missing:
                        console.print(f"[bold yellow]Missing dependencies:[/bold yellow] {', '.join(missing)}")
                    
                    # Provide installation instructions
                    console.print("[bold yellow]Please install the optional ML dependencies:[/bold yellow]")
                    print("  pip install vaahai[ml]")
                    
                    # Special instructions for macOS users with XGBoost issues
                    if platform.system() == "Darwin" and "xgboost+openmp" in missing:
                        console.print("[bold yellow]For macOS users with XGBoost OpenMP issues:[/bold yellow]")
                        print("  brew install libomp")
                        print("  pip install vaahai[ml]")
                    
                    sys.exit(1)
                
                return stub_command
            
            # Register the stub command with the correct name
            stub_func = create_stub_command(cmd_name)
            app.command(name=cmd_name, help=f"{cmd_name.capitalize()} (requires ML dependencies)")(stub_func)

# Register core commands (no ML dependencies)
register_core_commands()

# Try to register ML-dependent commands
register_ml_commands()

# Register stub commands for any ML commands that couldn't be registered
register_stub_commands()

# For direct script execution
if __name__ == "__main__":
    sys.exit(main())
