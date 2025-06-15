"""
VaahAI configuration warning utilities.

This module provides utilities for displaying configuration warnings
in CLI commands when VaahAI is not properly configured.
"""

from typing import Optional, List
from pathlib import Path

from rich.panel import Panel
from rich.text import Text

from vaahai.cli.utils.console import print_warning, print_error, console
from vaahai.utils.config_validator import ConfigValidator, ValidationLevel, ValidationResult


def display_config_warnings(
    config_path: Optional[Path] = None,
    show_all: bool = False,
    always_show_init_tip: bool = True,
) -> bool:
    """
    Display configuration warnings if VaahAI is not properly configured.
    
    Args:
        config_path (Optional[Path]): Path to a specific configuration file
        show_all (bool): Whether to show all validation results, not just errors
        always_show_init_tip (bool): Whether to always show the initialization tip
            even if there are no errors
            
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    # Skip if VaahAI is configured and we don't need to show all results
    if not show_all and ConfigValidator.is_configured() and not always_show_init_tip:
        return True
    
    # Create validator and run validation
    validator = ConfigValidator(config_path)
    is_valid, results = validator.validate()
    
    # Filter results based on show_all flag
    if not show_all:
        # Only show errors and warnings
        results = [r for r in results if r.level in (ValidationLevel.ERROR, ValidationLevel.WARNING) or not r.valid]
    
    # If there are no results to show and we don't need the init tip, exit early
    if not results and not always_show_init_tip:
        return is_valid
    
    # Group results by level
    errors = [r for r in results if r.level == ValidationLevel.ERROR]
    warnings = [r for r in results if r.level == ValidationLevel.WARNING]
    infos = [r for r in results if r.level == ValidationLevel.INFO and (show_all or not r.valid)]
    
    # If there's any error or warning, or we should always show the tip
    if errors or warnings or always_show_init_tip:
        # Only create heading if there's something to show
        if errors or warnings or infos:
            config_status = "⚠️ Configuration Issues" if not is_valid else "✅ Configuration Status"
            console.print(f"\n[bold yellow]{config_status}[/bold yellow]")
        
        # Display errors
        for error in errors:
            print_error(error.message)
        
        # Display warnings
        for warning in warnings:
            print_warning(warning.message)
        
        # Display infos
        for info in infos:
            status = "✅" if info.valid else "ℹ️"
            console.print(f"{status} {info.message}")
        
        # Always show initialization tip if requested
        if not is_valid or always_show_init_tip:
            init_tip = Panel(
                Text.from_markup(
                    "Run [bold cyan]vaahai config init[/bold cyan] to set up VaahAI configuration"
                ),
                title="Configuration Tip",
                border_style="yellow",
                padding=(1, 2),
            )
            console.print(init_tip)
    
    return is_valid


def check_for_unconfigured_vaahai(quiet: bool = False) -> bool:
    """
    Check if VaahAI is configured and display a warning if not.
    
    This is a simpler version of display_config_warnings intended for use
    at the start of CLI commands.
    
    Args:
        quiet (bool): Whether to suppress warnings
        
    Returns:
        bool: True if VaahAI is configured, False otherwise
    """
    if ConfigValidator.is_configured():
        return True
    
    if not quiet:
        print_warning(
            "⚠️ VaahAI is not configured! Some features may not work properly.\n"
            "Run 'vaahai config init' to set up VaahAI configuration."
        )
    
    return False
