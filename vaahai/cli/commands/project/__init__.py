"""
Project command group for VaahAI CLI.

This module contains commands for analyzing and working with code projects,
including code review and audit functionality.
"""

import typer
from vaahai.cli.commands.review.command import review_app
from vaahai.cli.commands.audit.command import audit_app

# Create the project commands group
project_app = typer.Typer(
    name="project",
    help="Project analysis commands",
    add_completion=True,
    no_args_is_help=True,
)

# Add commands to the project group
project_app.add_typer(review_app, name="review")
project_app.add_typer(audit_app, name="audit")
