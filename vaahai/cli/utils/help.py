"""
Custom help formatting utilities for VaahAI CLI.

This module provides utilities for enhancing Typer's help output with Rich formatting.
"""

from typing import Any, List, Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()


def custom_callback(ctx: typer.Context):
    """
    Custom callback for the main CLI app to enhance help output.
    
    Args:
        ctx: Typer context object
    """
    if ctx.invoked_subcommand is None:
        show_custom_help(ctx)


def show_custom_help(ctx: typer.Context):
    """
    Display custom formatted help using Rich.
    
    Args:
        ctx: Typer context object
    """
    # Get the command name
    command_name = ctx.command.name or "vaahai"
    
    # Create header
    header = Text()
    header.append(f"\n{command_name} ", style="bold cyan")
    header.append("- A multi AI agent CLI tool using Microsoft Autogen Framework\n", style="italic")
    
    # Create usage section
    usage = Text("Usage: ", style="bold")
    usage.append(f"{command_name} [OPTIONS] COMMAND [ARGS]...\n\n")
    
    # Create commands table
    commands_table = Table(title="Commands", box=None, padding=(0, 2))
    commands_table.add_column("Command", style="cyan")
    commands_table.add_column("Description")
    
    # Add commands to table
    for name, command in sorted(ctx.command.commands.items()):
        commands_table.add_row(name, command.help or "")
    
    # Create options table
    options_table = Table(title="Options", box=None, padding=(0, 2))
    options_table.add_column("Option", style="green")
    options_table.add_column("Description")
    
    # Add options to table
    for param in ctx.command.params:
        options = []
        for opt in param.opts:
            options.append(opt)
        options_str = ", ".join(options)
        options_table.add_row(options_str, param.help or "")
    
    # Print everything
    console.print(header)
    console.print(usage)
    console.print(commands_table)
    console.print(options_table)
    console.print("\nRun a command with --help to see command-specific options.\n")
