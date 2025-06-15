"""
VaahAI developer review command implementation.

This module contains the implementation of the developer review command,
which provides enhanced diagnostics and debugging information for code review.
"""

import os
import sys
import time
import logging
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from vaahai.cli.utils.console import (
    print_error,
    print_info,
    print_panel,
    print_success,
    print_warning,
)
from vaahai.cli.utils.help import CustomHelpCommand, create_typer_app
from vaahai.cli.utils.config_warnings import display_config_warnings
from vaahai.cli.commands.review.command import run as standard_review_run
from vaahai.config.manager import ConfigManager

# Set up logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)

# Create a logger for this module
logger = logging.getLogger("vaahai.dev_review")

# Create a rich console for formatted output
console = Console()

# Create the dev_review command app
dev_review_app = create_typer_app(
    name="dev-review",
    help="Developer review command with enhanced diagnostics",
    add_completion=True,
    no_args_is_help=True,
)


class DebugLevel(str, Enum):
    """Debug level options for the developer review command."""
    OFF = "off"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"


@dev_review_app.command("run", cls=CustomHelpCommand)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(
        ...,
        help="Path to file or directory to review",
    ),
    debug_level: DebugLevel = typer.Option(
        DebugLevel.INFO,
        "--debug-level",
        "-d",
        help="Debug level for diagnostics output",
    ),
    show_config: bool = typer.Option(
        False,
        "--show-config",
        "-c",
        help="Show configuration details before review",
    ),
    show_steps: bool = typer.Option(
        False,
        "--show-steps",
        "-s",
        help="Show detailed review steps and timing",
    ),
    log_file: Optional[Path] = typer.Option(
        None,
        "--log-file",
        "-l",
        help="Path to save diagnostic logs",
    ),
    format: Optional[str] = typer.Option(
        None,
        "--format",
        "-f",
        help="Output format (rich, markdown, html, interactive)",
    ),
    apply_changes: bool = typer.Option(
        False,
        "--apply-changes",
        "-a",
        help="Apply suggested changes to files",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show changes without applying them",
    ),
    backup_dir: Optional[Path] = typer.Option(
        None,
        "--backup-dir",
        help="Directory to store backups of modified files",
    ),
    no_confirm: bool = typer.Option(
        False,
        "--no-confirm",
        help="Don't ask for confirmation before applying changes",
    ),
):
    """
    Run a code review with enhanced diagnostics and debugging information.

    This command extends the standard review command with additional
    diagnostics, logging, and debug information useful for developers
    and contributors to VaahAI.
    
    Examples:
        vaahai dev-review run ./my-file.py
        vaahai dev-review run ./my-project --debug-level debug --show-steps
        vaahai dev-review run ./my-file.py --log-file ./review_debug.log
    """
    start_time = time.time()
    
    # Configure logging based on debug level
    if debug_level == DebugLevel.OFF:
        log_level = logging.WARNING
    elif debug_level == DebugLevel.INFO:
        log_level = logging.INFO
    elif debug_level == DebugLevel.DEBUG:
        log_level = logging.DEBUG
    elif debug_level == DebugLevel.TRACE:
        log_level = logging.DEBUG  # Python doesn't have TRACE, use DEBUG
        os.environ["VAAHAI_TRACE"] = "1"  # Set environment variable for trace-level logging
    
    # Set log level for our logger
    logger.setLevel(log_level)
    
    # Configure file logging if requested
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file}")
    
    # Log basic information
    logger.info(f"Starting developer review of: {path}")
    logger.info(f"Debug level: {debug_level.value}")
    logger.debug(f"Command context: {ctx.obj}")
    
    # Check configuration status
    if show_config or debug_level in (DebugLevel.DEBUG, DebugLevel.TRACE):
        logger.info("Checking configuration status...")
        config_valid = display_config_warnings(show_all=True)
        if not config_valid:
            logger.warning("Configuration validation failed")
        
        # Show detailed configuration if in debug mode
        if debug_level in (DebugLevel.DEBUG, DebugLevel.TRACE):
            try:
                config_manager = ConfigManager()
                config_data = config_manager.get_all()
                logger.debug("Current configuration:")
                for section, values in config_data.items():
                    if section == "providers":
                        # Mask API keys in provider section
                        providers_copy = {}
                        for provider, provider_config in values.items():
                            provider_copy = provider_config.copy()
                            if "api_key" in provider_copy:
                                provider_copy["api_key"] = "********"
                            providers_copy[provider] = provider_copy
                        logger.debug(f"  {section}: {providers_copy}")
                    else:
                        logger.debug(f"  {section}: {values}")
            except Exception as e:
                logger.error(f"Error retrieving configuration: {e}")
    
    # Show system information
    if debug_level in (DebugLevel.DEBUG, DebugLevel.TRACE):
        logger.debug("System information:")
        logger.debug(f"  Python version: {sys.version}")
        logger.debug(f"  Platform: {sys.platform}")
        logger.debug(f"  Current directory: {os.getcwd()}")
        logger.debug(f"  Environment variables:")
        for key, value in os.environ.items():
            if key.startswith("VAAHAI_"):
                if "KEY" in key or "TOKEN" in key or "SECRET" in key:
                    logger.debug(f"    {key}: ********")
                else:
                    logger.debug(f"    {key}: {value}")
    
    # Create a progress display for the review process
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.fields[status]}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        # Add a task for the overall review process
        review_task = progress.add_task("[bold]Running developer review...", total=None, status="In progress")
        
        try:
            # Set up step timing if requested
            if show_steps:
                os.environ["VAAHAI_STEP_TIMING"] = "1"
            
            # Instead of trying to pass parameters directly to standard_review_run,
            # create a wrapper function that handles the parameters correctly
            def run_review():
                # Create a modified version of the standard review command with our parameters
                from vaahai.cli.commands.review.command import run as standard_run
                from pathlib import Path
                
                # Convert path to Path object if it's a string
                path_obj = Path(path) if isinstance(path, str) else path
                
                # Call the standard review command directly with our parameters
                return standard_run(
                    path=path_obj,
                    depth="standard",  # Default to standard depth
                    focus=None,  # Don't pass focus to avoid OptionInfo issues
                    severity=None,  # Don't pass severity to avoid OptionInfo issues
                    debug=debug_level != DebugLevel.OFF,
                    format=format,
                    apply_changes=apply_changes,
                    dry_run=dry_run,
                    backup_dir=backup_dir,
                    no_confirm=no_confirm,
                )
            
            # Run the review using our wrapper function
            logger.info("Starting review process...")
            result = run_review()
            
            # Update progress
            progress.update(review_task, status="Complete")
            
            # Log completion
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"Review completed in {duration:.2f} seconds")
            
            # Show detailed timing information if requested
            if show_steps and hasattr(result, "step_timings") and result.step_timings:
                timing_table = Table(title="Review Step Timings")
                timing_table.add_column("Step", style="cyan")
                timing_table.add_column("Duration (s)", style="green", justify="right")
                timing_table.add_column("% of Total", style="yellow", justify="right")
                
                for step, step_time in result.step_timings.items():
                    percentage = (step_time / duration) * 100
                    timing_table.add_row(step, f"{step_time:.2f}", f"{percentage:.1f}%")
                
                console.print(timing_table)
            
            return result
            
        except Exception as e:
            # Update progress
            progress.update(review_task, status="Failed")
            
            # Log the error with traceback
            logger.exception(f"Error during review: {e}")
            
            # Show error panel
            print_error(f"Developer review failed: {e}")
            
            # Re-raise if in debug mode for full traceback
            if debug_level in (DebugLevel.DEBUG, DebugLevel.TRACE):
                raise
            
            return 1
