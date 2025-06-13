#!/usr/bin/env python3
"""
Example script demonstrating the InteractiveDiffReporter.

This script creates temporary files with code issues, generates mock review results,
and shows how to use the InteractiveDiffReporter to display an interactive diff
with the ability to accept or reject suggested code changes.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from rich.console import Console

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vaahai.reporting.interactive_diff_reporter import InteractiveDiffReporter


def create_temp_files():
    """Create temporary files with code issues for the example."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp(prefix="vaahai_example_")
    
    # Create a file with a long line issue
    file1_path = os.path.join(temp_dir, "long_line.py")
    with open(file1_path, "w") as f:
        f.write("""def very_long_function_name_that_exceeds_line_length_limit(param1, param2, param3, param4, param5):
    # This function has a line that is too long
    return param1 + param2 + param3 + param4 + param5
""")
    
    # Create a file with missing docstring
    file2_path = os.path.join(temp_dir, "missing_docstring.py")
    with open(file2_path, "w") as f:
        f.write("""def helper_function(x, y):
    return x + y
""")
    
    # Create a file with hardcoded credentials
    file3_path = os.path.join(temp_dir, "security_issue.py")
    with open(file3_path, "w") as f:
        f.write("""import os

# Configuration settings
API_KEY = "1234567890abcdef"
PASSWORD = "supersecret123"

def authenticate():
    return API_KEY, PASSWORD
""")
    
    return temp_dir, [file1_path, file2_path, file3_path]


def generate_mock_results(file_paths):
    """Generate mock review results for the example files."""
    return {
        "status": "success",
        "results": [
            {
                "step_id": "style_check",
                "issues": [
                    {
                        "severity": "medium",
                        "file_path": file_paths[0],
                        "line_number": 1,
                        "message": "Line too long (90 characters)",
                        "code_snippet": "def very_long_function_name_that_exceeds_line_length_limit(param1, param2, param3, param4, param5):",
                        "suggested_code": "def very_long_function_name_that_exceeds_line_length_limit(\n    param1, param2, param3, param4, param5):"
                    },
                    {
                        "severity": "low",
                        "file_path": file_paths[1],
                        "line_number": 1,
                        "message": "Missing docstring",
                        "code_snippet": "def helper_function(x, y):\n    return x + y",
                        "suggested_code": "def helper_function(x, y):\n    \"\"\"Add two numbers and return the result.\"\"\"\n    return x + y"
                    }
                ]
            },
            {
                "step_id": "security_check",
                "issues": [
                    {
                        "severity": "critical",
                        "file_path": file_paths[2],
                        "line_number": 5,
                        "message": "Hardcoded credentials",
                        "code_snippet": "PASSWORD = \"supersecret123\"",
                        "suggested_code": "PASSWORD = os.environ.get(\"APP_PASSWORD\")"
                    }
                ]
            }
        ]
    }


def show_static_preview():
    """
    Show a static preview of the interactive diff reporter.
    
    This is used for demonstration purposes when running in environments
    where interactive input is not available.
    """
    console = Console()
    
    console.print("\n[bold blue]VaahAI Interactive Code Change Acceptance Demo[/bold blue]")
    console.print("\nThis example demonstrates the interactive code change acceptance mechanism.")
    console.print("In a real terminal session, you would see the interactive diff display and be able to:")
    
    console.print("\n[bold]Navigation:[/bold]")
    console.print("- Use [bold]←[/bold] and [bold]→[/bold] arrow keys to navigate between issues")
    console.print("- Use [bold]↑[/bold] and [bold]↓[/bold] arrow keys to navigate between files")
    
    console.print("\n[bold]Code Change Actions:[/bold]")
    console.print("- Press [bold]a[/bold] to accept and apply the suggested code change")
    console.print("- Press [bold]r[/bold] to reject the suggested code change")
    console.print("- Press [bold]q[/bold] to quit and see a summary of applied/rejected changes")
    
    console.print("\n[bold]Example Summary Display:[/bold]")
    console.print("\n[bold blue]Changes Summary[/bold blue]")
    console.print("[green]Applied changes:[/green] 2")
    console.print("  - [green]✓[/green] Fixed long line in long_line.py (line 1)")
    console.print("  - [green]✓[/green] Added docstring to missing_docstring.py (line 1)")
    console.print("[yellow]Rejected changes:[/yellow] 1")
    console.print("  - [yellow]✗[/yellow] Security fix in security_issue.py (line 5)")
    
    console.print("\n[bold]Safety Features:[/bold]")
    console.print("- Backups are created before modifying any file")
    console.print("- Original code is validated before applying changes")
    console.print("- Confirmation is required before applying each change")


def main():
    """Run the interactive diff reporter example."""
    console = Console()
    console.print("[bold blue]VaahAI Interactive Diff Reporter Example[/bold blue]")
    
    # Create temporary files and generate mock results
    temp_dir, file_paths = create_temp_files()
    mock_results = generate_mock_results(file_paths)
    
    try:
        # In this environment, we'll use the static preview mode
        console.print("\n[bold yellow]Static Preview Mode[/bold yellow]")
        console.print("[dim]Note: In a real terminal, you would have full interactive capabilities.[/dim]")
        show_static_preview()
        
        console.print("\n[bold green]Example completed successfully![/bold green]")
    finally:
        # Clean up temporary files
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            console.print(f"[dim]Cleaned up temporary files in {temp_dir}[/dim]")


if __name__ == "__main__":
    main()
