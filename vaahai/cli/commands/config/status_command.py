"""
VaahAI config status command implementation.

This module contains the implementation of the config status command,
which is used to check and display the status of VaahAI configuration.
"""

from pathlib import Path
from typing import Optional

import typer

from vaahai.cli.utils.help import CustomHelpCommand
from vaahai.cli.utils.config_warnings import display_config_warnings


def status_command(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, 
        "--verbose", 
        "-v", 
        help="Show all configuration validation results, not just errors"
    ),
):
    """
    Check and display VaahAI configuration status.
    
    This command validates the VaahAI configuration and displays any issues 
    or warnings that might affect VaahAI's operation.
    """
    # Get config_file from context if available
    config_path = None
    if ctx.obj and "config_file" in ctx.obj:
        config_file = ctx.obj["config_file"]
        if config_file:
            config_path = Path(config_file)
    
    # Display configuration warnings with verbose output if requested
    is_valid = display_config_warnings(
        config_path=config_path,
        show_all=verbose,
        always_show_init_tip=False,
    )
    
    return is_valid  # Return validation status for CLI exit code
