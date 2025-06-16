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
from vaahai.cli.utils.warning_system import check_and_display_warnings
from vaahai.cli.commands.review.command import run as standard_review_run
from vaahai.config.manager import ConfigManager
from vaahai.agents.base.agent_factory import AgentFactory

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
    show_model_info: bool = typer.Option(
        False,
        "--show-model-info",
        "-m",
        help="Show LLM model information for each step",
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
    depth: str = typer.Option(
        "standard",
        "--depth",
        help="Depth of the review (quick, standard, thorough)",
    ),
    focus: Optional[str] = typer.Option(
        None,
        "--focus",
        help="Focus area for the review (style, security, performance)",
    ),
    severity: Optional[str] = typer.Option(
        None,
        "--severity",
        help="Minimum severity level (critical, high, medium, low)",
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
        vaahai dev review ./my-file.py
        vaahai dev review ./my-project --debug-level debug --show-steps
        vaahai dev review ./my-file.py --log-file ./review_debug.log
    """
    # Set up logging based on debug level
    if debug_level == DebugLevel.DEBUG:
        logger.setLevel(logging.DEBUG)
    elif debug_level == DebugLevel.TRACE:
        logger.setLevel(logging.DEBUG)  # Python doesn't have TRACE, use DEBUG
    elif debug_level == DebugLevel.INFO:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    
    # Configure log file if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
    
    logger.info(f"Starting developer review of {path}")
    logger.debug(f"Debug level: {debug_level}")
    
    # Record start time for performance measurement
    start_time = time.time()
    
    # Show configuration if requested
    if show_config:
        display_configuration()
    
    # Show model information if requested (placeholder for P4-T5)
    if show_model_info:
        display_model_information()
    
    # Create progress display
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[bold]{task.fields[status]}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Add a task for the review process
        review_task = progress.add_task(
            "Running developer review...", 
            total=1, 
            status="In Progress"
        )
        
        try:
            # Call the standard review command with additional debug information
            result = standard_review_run(
                path=Path(path),
                depth=depth,
                focus=focus,
                severity=severity,
                debug=debug_level != DebugLevel.OFF,  # Convert debug_level to boolean debug flag
                format=format,
                apply_changes=apply_changes,
                dry_run=dry_run,
                backup_dir=str(backup_dir) if backup_dir else None,
                no_confirm=no_confirm,
            )
            
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
            
            # Return exit code 1 to indicate failure
            return 1


def display_configuration():
    """Display the current configuration details."""
    try:
        config_manager = ConfigManager()
        
        # Get configuration details
        provider = config_manager.get_current_provider()
        model = config_manager.get_model(provider)
        docker_enabled = config_manager.get("docker.enabled", False)
        docker_image = config_manager.get("docker.image", "")
        docker_memory = config_manager.get("docker.memory", "")
        
        # Create a table for configuration display
        config_table = Table(title="VaahAI Configuration")
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="green")
        
        # Add configuration details to the table
        config_table.add_row("Provider", provider)
        config_table.add_row("Model", model)
        config_table.add_row("Docker Enabled", str(docker_enabled))
        
        if docker_enabled:
            config_table.add_row("Docker Image", docker_image)
            config_table.add_row("Docker Memory", docker_memory)
        
        # Display the table
        console.print(config_table)
        
        # Check for configuration warnings
        check_and_display_warnings(quiet=False)
        
    except Exception as e:
        logger.exception(f"Error displaying configuration: {e}")
        print_error(f"Failed to display configuration: {e}")


def display_model_information():
    """Display information about the LLM model being used (placeholder for P4-T5)."""
    try:
        config_manager = ConfigManager()
        provider = config_manager.get_current_provider()
        model = config_manager.get_model(provider)
        
        print_panel(
            f"[bold]Provider:[/bold] {provider}\n"
            f"[bold]Model:[/bold] {model}\n"
            f"[bold]Note:[/bold] Detailed model information will be available in a future update.",
            title="LLM Model Information",
            style="blue",
        )
        
    except Exception as e:
        logger.exception(f"Error displaying model information: {e}")
        print_error(f"Failed to display model information: {e}")
