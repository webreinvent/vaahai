"""
VaahAI developer review command implementation.

This module contains the implementation of the developer review command,
which provides enhanced diagnostics and debugging information for code review.
"""

import os
import sys
import time
import logging
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.box import Box, ROUNDED
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from vaahai.cli.utils.console import (
    print_error,
    print_info,
    print_panel,
    print_success,
    print_warning,
)
from vaahai.cli.utils.help import CustomHelpCommand, create_typer_app
from vaahai.cli.utils.warning_system import (
    WarningSystem, WarningCategory, WarningLevel, WarningMessage
)
from vaahai.config.manager import ConfigManager
from vaahai.config.llm_utils import get_api_key_from_env
from vaahai.utils.config_validator import ConfigValidator, ValidationLevel
from vaahai.config.utils import get_user_config_dir, get_project_config_dir
from vaahai.cli.commands.review.command import run as standard_review_run
from vaahai.agents.base.agent_factory import AgentFactory

# Create console for rich output
console = Console()

# Set up logger
logger = logging.getLogger("vaahai.dev_review")

# Create Typer app
dev_review_app = create_typer_app(
    name="review",
    help="Developer review command with enhanced diagnostics",
    add_completion=True,
    no_args_is_help=True,
)


class DebugLevel(str, Enum):
    """Debug level options for the developer review command."""
    OFF = "off"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"


def configure_logging(debug_level: DebugLevel, log_file: Optional[Path] = None):
    """
    Configure logging based on debug level and optional log file.
    
    Args:
        debug_level: The debug level to set
        log_file: Optional path to save logs to a file
    """
    # Set log level based on debug level
    if debug_level == DebugLevel.DEBUG:
        log_level = logging.DEBUG
    elif debug_level == DebugLevel.TRACE:
        log_level = logging.DEBUG  # Python doesn't have TRACE, use DEBUG
    elif debug_level == DebugLevel.INFO:
        log_level = logging.INFO
    else:  # OFF
        log_level = logging.WARNING
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add Rich handler for console output
    rich_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=False,
    )
    rich_handler.setLevel(log_level)
    root_logger.addHandler(rich_handler)
    
    # Add file handler if log file is specified
    if log_file:
        try:
            # Create directory if it doesn't exist
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Add file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            root_logger.addHandler(file_handler)
            
            logger.info(f"Logging to file: {log_file}")
        except Exception as e:
            logger.error(f"Failed to set up log file: {e}")


@dev_review_app.command("run", cls=CustomHelpCommand)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(
        ...,
        help="Path to file or directory to review",
    ),
    debug_level: DebugLevel = typer.Option(
        DebugLevel.INFO,
        "--debug-level",
        "-d",
        help="Debug level for diagnostics output",
    ),
    show_config: bool = typer.Option(
        False,
        "--show-config",
        "-c",
        help="Show configuration details before review",
    ),
    show_steps: bool = typer.Option(
        False,
        "--show-steps",
        "-s",
        help="Show detailed review steps and timing",
    ),
    show_model_info: bool = typer.Option(
        False,
        "--show-model-info",
        "-m",
        help="Show LLM model information for each step",
    ),
    log_file: Optional[Path] = typer.Option(
        None,
        "--log-file",
        "-l",
        help="Path to save diagnostic logs",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Output format (text, json, markdown, html)",
    ),
    depth: Optional[int] = typer.Option(
        None,
        "--depth",
        help="Maximum depth for directory traversal",
    ),
    focus: Optional[str] = typer.Option(
        None,
        "--focus",
        help="Focus on specific aspects (comma-separated)",
    ),
    severity: Optional[str] = typer.Option(
        None,
        "--severity",
        help="Minimum severity level to report",
    ),
    apply_changes: bool = typer.Option(
        False,
        "--apply",
        "-a",
        help="Apply suggested changes",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show changes without applying them",
    ),
    backup_dir: Optional[Path] = typer.Option(
        None,
        "--backup-dir",
        help="Directory to store backups before applying changes",
    ),
    no_confirm: bool = typer.Option(
        False,
        "--no-confirm",
        help="Skip confirmation prompts",
    ),
):
    """
    Run the review command with enhanced developer diagnostics.
    
    This command extends the standard review command with additional
    debugging and diagnostic options.
    """
    # Record start time for overall timing
    start_time = time.time()
    
    # Configure logging based on debug level
    configure_logging(debug_level, log_file)
    
    # Log command invocation
    logger.info(f"Running dev review command with debug level: {debug_level.name}")
    logger.debug(f"Command arguments: path={path}, show_config={show_config}, show_steps={show_steps}, show_model_info={show_model_info}")
    
    # Show configuration if requested
    if show_config:
        display_configuration()
    
    # Show model information if requested
    if show_model_info:
        display_model_information()
    
    # Create progress display
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.fields[status]}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Add a task for the review process
        review_task = progress.add_task(
            "Running developer review...", 
            total=1, 
            status="In Progress"
        )
        
        try:
            # Call the standard review command with additional debug information
            result = standard_review_run(
                path=Path(path),
                depth=depth,
                focus=focus,
                severity=severity,
                debug=debug_level != DebugLevel.OFF,  # Convert debug_level to boolean debug flag
                format=format,
                apply_changes=apply_changes,
                dry_run=dry_run,
                backup_dir=str(backup_dir) if backup_dir else None,
                no_confirm=no_confirm,
                collect_step_timings=show_steps,  # Enable step timing collection if requested
                track_model_usage=show_model_info,  # Enable model tracking if requested
            )
            
            # Update progress
            progress.update(review_task, status="Complete")
            
            # Log completion
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"Review completed in {duration:.2f} seconds")
            
            # Show detailed timing information if requested
            if show_steps and hasattr(result, "step_timings") and result.step_timings:
                timing_table = Table(title="Review Step Timings")
                timing_table.add_column("Step ID", style="cyan")
                timing_table.add_column("Step Name", style="green")
                timing_table.add_column("Duration (s)", style="yellow", justify="right")
                
                for step_id, duration in result.step_timings.items():
                    step_name = next((s.name for s in result.steps if s.id == step_id), step_id)
                    timing_table.add_row(step_id, step_name, f"{duration:.2f}")
                
                console.print(timing_table)
            
            # Show model information for each step if requested
            if show_model_info and hasattr(result, "model_tracker"):
                display_step_model_information(result.model_tracker)
            
            return result
            
        except Exception as e:
            # Update progress to show error
            progress.update(review_task, status="Error")
            
            # Log the error
            logger.exception(f"Error running review: {e}")
            
            # Display error message
            print_error(f"Error running review: {e}")
            
            # Re-raise the exception
            raise


def display_configuration():
    """Display the current configuration settings with detailed verification reporting."""
    console = Console()
    
    # Get configuration paths
    user_config_dir = get_user_config_dir()
    user_config_file = user_config_dir / "config.toml"
    project_config_dir = get_project_config_dir()
    project_config_file = project_config_dir / "config.toml" if project_config_dir else None
    
    # Debug information about config files
    logger.debug(f"User config directory: {user_config_dir} (exists: {user_config_dir.exists()})")
    logger.debug(f"User config file: {user_config_file} (exists: {user_config_file.exists()})")
    if project_config_dir:
        logger.debug(f"Project config directory: {project_config_dir} (exists: {project_config_dir.exists()})")
        if project_config_file:
            logger.debug(f"Project config file: {project_config_file} (exists: {project_config_file.exists()})")
    
    # Create config manager and validator
    config_manager = ConfigManager()
    config_validator = ConfigValidator(config_manager)
    
    # Check if VaahAI is configured
    is_configured = config_validator.is_configured()
    
    if not is_configured:
        console.print(Panel("[bold red]VaahAI configuration file is missing.[/]", 
                           title="[bold red]Configuration Error[/]", 
                           border_style="red"))
        console.print("Please run [bold]vaahai config init[/] to set up your configuration.")
        return
    
    # Run full validation
    is_valid, validation_results = config_validator.validate()
    
    # Display overall configuration status
    status_color = "green" if is_valid else "yellow"
    status_text = "Valid" if is_valid else "Valid with warnings"
    
    console.print(Panel(
        f"[bold {status_color}]VaahAI Configuration Status: {status_text}[/]",
        title="[bold blue]Configuration Verification[/]",
        border_style=status_color
    ))
    
    # Create tables for different configuration aspects
    
    # 1. Configuration Files Table
    files_table = Table(title="Configuration Files", box=ROUNDED)
    files_table.add_column("File Type", style="cyan")
    files_table.add_column("Path", style="blue")
    files_table.add_column("Status", style="green")
    
    # Add user config file
    user_file_status = "[green]✓ Exists[/]" if user_config_file.exists() else "[red]✗ Missing[/]"
    files_table.add_row("User Config", str(user_config_file), user_file_status)
    
    # Add project config file if applicable
    if project_config_file:
        project_file_status = "[green]✓ Exists[/]" if project_config_file.exists() else "[yellow]! Not found[/]"
        files_table.add_row("Project Config", str(project_config_file), project_file_status)
    
    console.print(files_table)
    
    # 2. LLM Provider Configuration
    try:
        # Get current provider and model
        provider = config_manager.get_current_provider()
        model = config_manager.get_model(provider)
        
        # Check if API key is set (don't display the actual key)
        api_key = config_manager.get_api_key(provider)
        api_key_set = api_key is not None and api_key != ""
        
        # Check if API key is from environment variable
        api_key_from_env = provider and get_api_key_from_env(provider) is not None
        
        # Get model capabilities and context length
        model_info = {}
        try:
            model_info = config_manager.get_model_info(model, provider)
        except Exception as e:
            logger.debug(f"Could not get model info: {e}")
        
        # Create LLM configuration table
        llm_table = Table(title="LLM Configuration", box=ROUNDED)
        llm_table.add_column("Setting", style="cyan")
        llm_table.add_column("Value", style="green")
        llm_table.add_column("Status", style="blue")
        
        # Add provider
        provider_status = "[green]✓ Set[/]" if provider else "[red]✗ Not set[/]"
        llm_table.add_row("Provider", provider or "Not set", provider_status)
        
        # Add model
        model_status = "[green]✓ Set[/]" if model else "[red]✗ Not set[/]"
        llm_table.add_row("Model", model or "Not set", model_status)
        
        # Add API key status (don't show the actual key)
        api_key_status = "[green]✓ Set[/]" if api_key_set else "[red]✗ Not set[/]"
        api_key_source = " [blue](from environment)[/]" if api_key_from_env else ""
        llm_table.add_row("API Key", "********" if api_key_set else "Not set", f"{api_key_status}{api_key_source}")
        
        # Add model capabilities if available
        if "capabilities" in model_info and model_info["capabilities"]:
            capabilities = ", ".join(model_info["capabilities"])
            llm_table.add_row("Capabilities", capabilities, "")
        
        # Add context length if available
        if "context_length" in model_info and model_info["context_length"]:
            context_length = f"{model_info['context_length']:,} tokens"
            llm_table.add_row("Context Length", context_length, "")
        
        console.print(llm_table)
        
        # 3. Docker Configuration
        docker_enabled = config_manager.get("docker.enabled", False)
        
        docker_table = Table(title="Docker Configuration", box=ROUNDED)
        docker_table.add_column("Setting", style="cyan")
        docker_table.add_column("Value", style="green")
        docker_table.add_column("Status", style="blue")
        
        docker_status = "[green]✓ Enabled[/]" if docker_enabled else "[yellow]! Disabled[/]"
        docker_table.add_row("Docker Enabled", str(docker_enabled), docker_status)
        
        if docker_enabled:
            docker_image = config_manager.get("docker.image", "")
            docker_memory = config_manager.get("docker.memory", "")
            
            image_status = "[green]✓ Set[/]" if docker_image else "[yellow]! Default will be used[/]"
            memory_status = "[green]✓ Set[/]" if docker_memory else "[yellow]! Default will be used[/]"
            
            docker_table.add_row("Docker Image", docker_image or "Default", image_status)
            docker_table.add_row("Docker Memory", docker_memory or "Default", memory_status)
        
        console.print(docker_table)
        
        # 4. Environment Variable Overrides
        env_vars = {}
        for env_key, env_value in os.environ.items():
            if env_key.startswith("VAAHAI_"):
                config_key = env_key[7:].lower().replace("_", ".")
                env_vars[config_key] = "********" if "api_key" in config_key.lower() else env_value
        
        if env_vars:
            env_table = Table(title="Environment Variable Overrides", box=ROUNDED)
            env_table.add_column("Config Key", style="cyan")
            env_table.add_column("Environment Variable", style="blue")
            env_table.add_column("Value", style="green")
            
            for config_key, value in env_vars.items():
                env_var = f"VAAHAI_{config_key.upper().replace('.', '_')}"
                env_table.add_row(config_key, env_var, value)
            
            console.print(env_table)
        
    except Exception as e:
        logger.error(f"Error getting LLM configuration: {e}")
        console.print("[bold yellow]Could not retrieve complete LLM configuration details.[/]")
    
    # 5. Validation Results
    if not is_valid or any(not result.valid for result in validation_results):
        validation_table = Table(title="Configuration Validation Issues", box=ROUNDED)
        validation_table.add_column("Level", style="cyan")
        validation_table.add_column("Key", style="blue")
        validation_table.add_column("Message", style="yellow")
        
        for result in validation_results:
            if not result.valid:
                level_style = {
                    ValidationLevel.ERROR: "red",
                    ValidationLevel.WARNING: "yellow",
                    ValidationLevel.INFO: "blue"
                }.get(result.level, "white")
                
                validation_table.add_row(
                    f"[{level_style}]{result.level.value.upper()}[/]",
                    result.key or "N/A",
                    result.message
                )
        
        console.print(validation_table)
    
    # Create a warning system instance
    warning_system = WarningSystem()
    
    # Add warnings based on validation results
    for result in validation_results:
        if not result.valid:
            level = {
                ValidationLevel.ERROR: WarningLevel.ERROR,
                ValidationLevel.WARNING: WarningLevel.WARNING,
                ValidationLevel.INFO: WarningLevel.INFO,
            }[result.level]
            
            # Add a warning based on the validation result
            warning_system.add_warning(
                WarningMessage(
                    level=level,
                    category=WarningCategory.CONFIGURATION,
                    message=result.message,
                    details=f"Key: {result.key}" if result.key else None,
                )
            )
    
    # Display the warnings
    warning_system.display_warnings(
        categories=[WarningCategory.CONFIGURATION],
        min_level=WarningLevel.WARNING,
        command_context="dev review"
    )


def display_model_information():
    """Display information about the LLM model configuration."""
    try:
        config_manager = ConfigManager()
        provider = config_manager.get_current_provider()
        model = config_manager.get_model(provider)
        
        # Get additional model configuration if available
        model_config = {}
        try:
            model_config = config_manager.get_provider_config(provider) or {}
        except Exception:
            pass
        
        # Create a panel with model information
        content = [
            f"[bold]Provider:[/bold] {provider}",
            f"[bold]Model:[/bold] {model}",
        ]
        
        # Add model configuration details if available
        if model_config:
            content.append("[bold]Configuration:[/bold]")
            for key, value in model_config.items():
                if key not in ["api_key", "secret", "token", "password"]:  # Skip sensitive information
                    content.append(f"  [cyan]{key}:[/cyan] {value}")
        
        print_panel(
            "\n".join(content),
            title="LLM Model Configuration",
            style="blue",
        )
        
    except Exception as e:
        logger.exception(f"Error displaying model information: {e}")
        print_error(f"Failed to display model information: {e}")


def display_step_model_information(model_tracker):
    """
    Display information about which LLM model was used for each review step.
    
    Args:
        model_tracker: The model tracker containing step model usage information
    """
    try:
        # Get all model usage information
        step_models = model_tracker.get_all_model_usage()
        
        if not step_models:
            print_panel(
                "No LLM model usage was recorded during the review process.",
                title="LLM Model Usage",
                style="blue",
            )
            return
        
        # Create a table for step model information
        model_table = Table(title="LLM Model Usage by Step")
        model_table.add_column("Step ID", style="cyan")
        model_table.add_column("Step Name", style="green")
        model_table.add_column("Provider", style="yellow")
        model_table.add_column("Model", style="magenta")
        model_table.add_column("Parameters", style="blue")
        
        # Add rows for each step
        for step_id, model_info in step_models.items():
            # Get step name if available
            step_name = model_info.get("step_name", step_id)
            
            # Extract model information
            provider = model_info.get("provider", "unknown")
            model_name = model_info.get("model_name", "unknown")
            
            # Format parameters
            parameters = []
            for key, value in model_info.items():
                if key not in ["provider", "model_name", "step_id", "step_name"]:
                    parameters.append(f"{key}={value}")
            
            # Add row to table
            model_table.add_row(
                step_id,
                step_name,
                provider,
                model_name,
                ", ".join(parameters) if parameters else "default"
            )
        
        # Print the table
        console.print(model_table)
        
        # Print model usage summary
        usage_summary = model_tracker.get_model_usage_summary()
        if usage_summary:
            summary_table = Table(title="Model Usage Summary")
            summary_table.add_column("Model", style="cyan")
            summary_table.add_column("Usage Count", style="yellow", justify="right")
            
            for model, count in usage_summary.items():
                summary_table.add_row(model, str(count))
            
            console.print(summary_table)
        
    except Exception as e:
        logger.exception(f"Error displaying step model information: {e}")
        print_error(f"Failed to display step model information: {e}")
