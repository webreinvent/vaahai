"""
VaahAI helloworld command implementation.

This module contains the implementation of the helloworld command,
which is used to test the proper functioning of the VaahAI CLI.
"""

import typer
from vaahai.cli.utils.console import print_panel, print_success, console

# Create the helloworld command group
helloworld_app = typer.Typer(
    name="helloworld",
    help="Test command to verify proper functioning of VaahAI",
    add_completion=False,
)


@helloworld_app.callback()
def callback():
    """
    Test command to verify proper functioning of VaahAI.
    """
    pass


@helloworld_app.command("run")
def run():
    """
    Run the helloworld command to test VaahAI functionality.
    """
    print_panel(
        "[bold green]Hello from VaahAI![/bold green]\n\n"
        "VaahAI CLI is working correctly.\n"
        "This is a placeholder for the actual helloworld command.",
        title="VaahAI Helloworld",
        style="green",
    )
    print_success("VaahAI CLI is ready to use!")
