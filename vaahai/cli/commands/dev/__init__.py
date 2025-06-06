"""
Development and testing commands for VaahAI CLI.

This module contains commands for development and testing purposes.
"""

import typer
from vaahai.cli.commands.helloworld.command import helloworld_app
from vaahai.cli.commands.dev.showcase import showcase_app
from vaahai.cli.commands.dev.prompts import prompts_app

# Create a Typer instance for the dev command group
dev_app = typer.Typer(help="Development and testing commands")

# Register subcommands
dev_app.add_typer(helloworld_app, name="helloworld")
dev_app.add_typer(showcase_app, name="showcase")
dev_app.add_typer(prompts_app, name="prompts")
