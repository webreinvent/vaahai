"""
Development command group for VaahAI CLI.

This module contains commands primarily used during development and testing,
including the helloworld command for verifying proper CLI functionality.
"""

import typer
from vaahai.cli.commands.helloworld.command import helloworld_app

# Create the development commands group
dev_app = typer.Typer(
    name="dev",
    help="Development and testing commands",
    add_completion=True,
    no_args_is_help=True,
)

# Add commands to the development group
dev_app.add_typer(helloworld_app, name="helloworld")
