"""
Template for VaahAI command implementation.

This template demonstrates how to implement a command with custom help formatting.
"""

import typer

from vaahai.cli.utils.console import console, print_panel, print_success
from vaahai.cli.utils.help import CustomHelpCommand, create_typer_app

# Create the command group with custom help formatting
app = create_typer_app(
    name="command_name",
    help="Description of the command",
    add_completion=False,
)


@app.callback()
def callback():
    """
    Callback for the command group.
    """
    pass


@app.command("subcommand", cls=CustomHelpCommand)
def subcommand(
    arg1: str = typer.Argument(..., help="Description of argument 1"),
    option1: bool = typer.Option(
        False, "--option1", "-o", help="Description of option 1"
    ),
):
    """
    Description of the subcommand.
    """
    # Command implementation here
    print_success("Command executed successfully!")
