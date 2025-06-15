#!/usr/bin/env python3
"""
Example script demonstrating the VaahAI configuration validation utility.

This script shows how to use the configuration validation utility to check
if the VaahAI configuration is valid and complete before running commands.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add the parent directory to the path so we can import vaahai
sys.path.insert(0, str(Path(__file__).parent.parent))

from vaahai.config.validation import (
    validate_configuration_exists,
    validate_configuration_complete,
    validate_for_command,
    get_validation_summary
)
from vaahai.config.manager import ConfigManager


def print_header(title):
    """Print a header with the given title."""
    console = Console()
    console.print(Panel(f"[bold blue]{title}[/bold blue]", expand=False))
    console.print()


def print_validation_result(is_valid, errors):
    """Print validation result."""
    console = Console()
    if is_valid:
        console.print("[bold green]✓ Configuration is valid![/bold green]")
    else:
        console.print("[bold red]✗ Configuration is invalid:[/bold red]")
        for error in errors:
            console.print(f"  [red]• {error}[/red]")
    console.print()


def main():
    """Main function demonstrating configuration validation."""
    console = Console()
    
    print_header("VaahAI Configuration Validation Example")
    
    # Check if configuration exists
    console.print("[bold]1. Checking if configuration exists...[/bold]")
    exists, message = validate_configuration_exists()
    if exists:
        console.print(f"[green]✓ {message}[/green]")
    else:
        console.print(f"[red]✗ {message}[/red]")
        console.print("[yellow]Run 'vaahai config init' to create a configuration file[/yellow]")
        return
    console.print()
    
    # Validate complete configuration
    console.print("[bold]2. Validating complete configuration...[/bold]")
    errors = validate_configuration_complete()
    print_validation_result(len(errors) == 0, errors)
    
    # Validate for specific commands
    commands = ["review", "audit", "helloworld"]
    for command in commands:
        console.print(f"[bold]3. Validating configuration for '{command}' command...[/bold]")
        valid, cmd_errors = validate_for_command(command)
        print_validation_result(valid, cmd_errors)
    
    # Get validation summary
    console.print("[bold]4. Getting validation summary...[/bold]")
    summary = get_validation_summary()
    
    # Display summary in a table
    table = Table(title="Configuration Validation Summary")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Valid", "✓ Yes" if summary["is_valid"] else "✗ No")
    table.add_row("Exists", "✓ Yes" if summary["exists"] else "✗ No")
    table.add_row("Provider", summary["provider"] or "[not set]")
    table.add_row("Model", summary["model"] or "[not set]")
    table.add_row("Error Count", str(summary["error_count"]))
    
    console.print(table)
    console.print()
    
    # If there are errors, display them
    if summary["errors"]:
        console.print("[bold red]Validation Errors:[/bold red]")
        for i, error in enumerate(summary["errors"], 1):
            console.print(f"  [red]{i}. {error}[/red]")
    
    # Show how to use validation in your code
    console.print("\n[bold]How to use validation in your code:[/bold]")
    console.print("""
# Check if configuration exists before running a command
exists, message = validate_configuration_exists()
if not exists:
    print(f"Error: {message}")
    print("Run 'vaahai config init' to set up configuration")
    return

# Validate configuration for a specific command
valid, errors = validate_for_command("review")
if not valid:
    print("Configuration is not valid for 'review' command:")
    for error in errors:
        print(f"- {error}")
    return

# Proceed with command execution
print("Configuration is valid, proceeding with command...")
    """)


if __name__ == "__main__":
    main()
