"""
Custom help formatting utilities for VaahAI CLI.

This module provides utilities for enhancing Typer's help output with Rich formatting.
"""

from typing import Any, List, Optional, Dict
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.box import ROUNDED

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
    
    # Create command groups table
    groups_table = Table(title="Command Groups", box=ROUNDED, padding=(0, 2), expand=True)
    groups_table.add_column("Group", style="magenta", no_wrap=True)
    groups_table.add_column("Description")
    groups_table.add_column("Example", style="green")
    
    # Command group examples dictionary
    group_examples: Dict[str, str] = {
        "core": f"{command_name} core config init",
        "project": f"{command_name} project review run ./my-project",
        "dev": f"{command_name} dev helloworld run",
    }
    
    # Add command groups to table
    group_commands = {
        "core": "Essential VaahAI commands",
        "project": "Project analysis commands",
        "dev": "Development and testing commands",
    }
    
    for name, description in sorted(group_commands.items()):
        example = group_examples.get(name, f"{command_name} {name}")
        groups_table.add_row(name, description, example)
    
    # Create commands table for backward compatibility
    commands_table = Table(title="Commands (Direct Access)", box=ROUNDED, padding=(0, 2), expand=True)
    commands_table.add_column("Command", style="cyan", no_wrap=True)
    commands_table.add_column("Description")
    commands_table.add_column("Example", style="green")
    
    # Command examples dictionary
    examples: Dict[str, str] = {
        "helloworld": f"{command_name} helloworld run",
        "config": f"{command_name} config init",
        "review": f"{command_name} review run ./my-project",
        "audit": f"{command_name} audit run ./my-project --security",
        "version": f"{command_name} version show",
    }
    
    # Filter out command groups from direct commands
    direct_commands = {}
    for name, command in sorted(ctx.command.commands.items()):
        if name not in group_commands:
            direct_commands[name] = command
    
    # Add commands to table
    for name, command in sorted(direct_commands.items()):
        example = examples.get(name, f"{command_name} {name}")
        commands_table.add_row(name, command.help or "", example)
    
    # Create options table
    options_table = Table(title="Global Options", box=ROUNDED, padding=(0, 2), expand=True)
    options_table.add_column("Option", style="green", no_wrap=True)
    options_table.add_column("Description")
    options_table.add_column("Default", style="dim")
    
    # Add options to table
    for param in ctx.command.params:
        options = []
        for opt in param.opts:
            options.append(opt)
        options_str = ", ".join(options)
        
        # Get default value if any
        default = ""
        if param.default is not None and param.default is not ...:
            default = str(param.default)
        
        options_table.add_row(options_str, param.help or "", default)
    
    # Create environment variables panel
    env_vars_md = """
    **Environment Variables:**
    
    * `VAAHAI_DEBUG=1` - Enable debug mode with full error tracebacks
    * `VAAHAI_CONFIG_DIR` - Override default config directory location
    """
    
    # Print everything
    console.print(Panel(header, border_style="cyan", expand=False))
    console.print(usage)
    console.print(groups_table)
    console.print(commands_table)
    console.print(options_table)
    console.print(Markdown(env_vars_md))
    console.print("\nRun a command with --help to see command-specific options and examples.\n")


def format_command_help(ctx: typer.Context):
    """
    Format help for a specific command.
    
    Args:
        ctx: Typer context object for the command
    """
    command = ctx.command
    command_path = " ".join(ctx.command_path.split())
    
    # Create header
    header = Text()
    header.append(f"\n{command_path}\n", style="bold cyan")
    
    if command.help:
        header.append(f"\n{command.help}\n", style="italic")
    
    # Create usage section
    usage = Text("Usage: ", style="bold")
    usage.append(f"{command_path} [OPTIONS]")
    
    if command.params:
        for param in command.params:
            if param.param_type_name == "argument":
                usage.append(f" {param.name.upper()}")
    
    usage.append("\n\n")
    
    # Create options table if there are options
    has_options = False
    for param in command.params:
        if param.param_type_name == "option":
            has_options = True
            break
    
    if has_options:
        options_table = Table(title="Options", box=ROUNDED, padding=(0, 2), expand=True)
        options_table.add_column("Option", style="green", no_wrap=True)
        options_table.add_column("Description")
        options_table.add_column("Default", style="dim")
        
        for param in command.params:
            if param.param_type_name == "option":
                options = []
                for opt in param.opts:
                    options.append(opt)
                options_str = ", ".join(options)
                
                # Get default value if any
                default = ""
                if param.default is not None and param.default is not ...:
                    default = str(param.default)
                
                options_table.add_row(options_str, param.help or "", default)
    
    # Create arguments table if there are arguments
    has_args = False
    for param in command.params:
        if param.param_type_name == "argument":
            has_args = True
            break
    
    if has_args:
        args_table = Table(title="Arguments", box=ROUNDED, padding=(0, 2), expand=True)
        args_table.add_column("Argument", style="cyan", no_wrap=True)
        args_table.add_column("Description")
        args_table.add_column("Type", style="dim")
        
        for param in command.params:
            if param.param_type_name == "argument":
                arg_type = getattr(param.type, "__name__", str(param.type))
                args_table.add_row(param.name, param.help or "", arg_type)
    
    # Print everything
    console.print(Panel(header, border_style="cyan", expand=False))
    console.print(usage)
    
    if has_args:
        console.print(args_table)
    
    if has_options:
        console.print(options_table)
    
    # Print subcommands if any
    if hasattr(command, "commands") and command.commands:
        subcommands_table = Table(title="Subcommands" if command.info.help or "" else "Commands", box=ROUNDED, padding=(0, 2), expand=True)
        subcommands_table.add_column("Command", style="cyan", no_wrap=True)
        subcommands_table.add_column("Description")
        
        for name, subcmd in sorted(command.commands.items()):
            subcommands_table.add_row(name, subcmd.help or "")
        
        console.print(subcommands_table)
        console.print("\nRun a subcommand with --help to see command-specific options.\n")
