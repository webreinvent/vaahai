"""
VaahAI CLI main entry point.

This module serves as the entry point for the VaahAI CLI application.
It defines the main Typer app instance and registers all command groups.
"""

import typer
from rich.console import Console

# Import command modules
from vaahai.cli.commands.helloworld.command import helloworld_app
from vaahai.cli.commands.config.command import config_app
from vaahai.cli.commands.review.command import review_app
from vaahai.cli.commands.audit.command import audit_app

# Create the main Typer app instance
app = typer.Typer(
    name="vaahai",
    help="A multi AI agent CLI tool using Microsoft Autogen Framework",
    add_completion=False,
)

# Create a rich console for formatted output
console = Console()

# Add command groups to the main app
app.add_typer(helloworld_app, name="helloworld")
app.add_typer(config_app, name="config")
app.add_typer(review_app, name="review")
app.add_typer(audit_app, name="audit")


@app.callback()
def callback():
    """
    VaahAI: A multi AI agent CLI tool using Microsoft Autogen Framework.
    """
    pass


if __name__ == "__main__":
    app()
