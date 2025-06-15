"""
VaahAI warning message system.

This module provides utilities for displaying warning messages
across all CLI commands when there are configuration issues,
missing dependencies, or other potential problems.
"""

from enum import Enum
from typing import Optional, List, Dict, Any, Union
from pathlib import Path

from rich.panel import Panel
from rich.text import Text
from rich.console import Console

from vaahai.cli.utils.console import console, print_warning, print_error, print_info
from vaahai.utils.config_validator import ConfigValidator, ValidationLevel, ValidationResult


class WarningCategory(Enum):
    """Categories for warning messages."""
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    PERMISSION = "permission"
    NETWORK = "network"
    PERFORMANCE = "performance"
    SECURITY = "security"
    COMPATIBILITY = "compatibility"
    GENERAL = "general"


class WarningLevel(Enum):
    """Warning severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class WarningMessage:
    """
    A warning message to be displayed to the user.
    
    Attributes:
        level (WarningLevel): Severity level of the warning
        category (WarningCategory): Category of the warning
        message (str): The warning message text
        details (Optional[str]): Additional details about the warning
        fix_command (Optional[str]): Command that can fix the issue
        docs_url (Optional[str]): URL to documentation about the issue
    """
    
    def __init__(
        self,
        level: WarningLevel,
        category: WarningCategory,
        message: str,
        details: Optional[str] = None,
        fix_command: Optional[str] = None,
        docs_url: Optional[str] = None,
    ):
        self.level = level
        self.category = category
        self.message = message
        self.details = details
        self.fix_command = fix_command
        self.docs_url = docs_url
    
    def __str__(self) -> str:
        """Return a string representation of the warning message."""
        prefix = {
            WarningLevel.ERROR: "❌",
            WarningLevel.WARNING: "⚠️",
            WarningLevel.INFO: "ℹ️",
        }[self.level]
        
        return f"{prefix} {self.message}"
    
    def get_rich_panel(self) -> Panel:
        """Get a Rich panel representation of the warning message."""
        content = []
        content.append(f"[bold]{self.message}[/bold]")
        
        if self.details:
            content.append(f"\n{self.details}")
        
        if self.fix_command:
            content.append(f"\n[cyan]Run: [bold]{self.fix_command}[/bold][/cyan]")
        
        if self.docs_url:
            content.append(f"\n[blue]Documentation: {self.docs_url}[/blue]")
        
        border_style = {
            WarningLevel.ERROR: "red",
            WarningLevel.WARNING: "yellow",
            WarningLevel.INFO: "blue",
        }[self.level]
        
        title = {
            WarningLevel.ERROR: "Error",
            WarningLevel.WARNING: "Warning",
            WarningLevel.INFO: "Information",
        }[self.level]
        
        category_title = f"{title} [{self.category.value.capitalize()}]"
        
        return Panel(
            Text.from_markup("\n".join(content)),
            title=category_title,
            border_style=border_style,
            padding=(1, 2),
        )


class WarningSystem:
    """
    System for managing and displaying warnings across CLI commands.
    
    This class collects warnings from various sources and displays them
    to the user at appropriate times.
    """
    
    def __init__(self, quiet: bool = False):
        """
        Initialize the warning system.
        
        Args:
            quiet (bool): Whether to suppress warnings
        """
        self.warnings: List[WarningMessage] = []
        self.quiet = quiet
        self.shown_warnings: Dict[str, bool] = {}  # Track which warnings have been shown
    
    def add_warning(self, warning: WarningMessage) -> None:
        """
        Add a warning to the system.
        
        Args:
            warning (WarningMessage): The warning to add
        """
        self.warnings.append(warning)
    
    def add_config_warnings(self) -> None:
        """Add configuration warnings based on ConfigValidator results."""
        validator = ConfigValidator()
        is_valid, results = validator.validate()
        
        for result in results:
            if not result.valid:
                level = {
                    ValidationLevel.ERROR: WarningLevel.ERROR,
                    ValidationLevel.WARNING: WarningLevel.WARNING,
                    ValidationLevel.INFO: WarningLevel.INFO,
                }[result.level]
                
                # Create more specific warning messages for configuration issues
                if "config file does not exist" in result.message.lower():
                    self.add_warning(
                        WarningMessage(
                            level=level,
                            category=WarningCategory.CONFIGURATION,
                            message="VaahAI configuration file is missing",
                            details="Please create a configuration file using 'vaahai config init' command.",
                            fix_command="vaahai config init",
                            docs_url="https://docs.vaahai.io/configuration",
                        )
                    )
                elif "api key" in result.message.lower():
                    provider = result.key.split(".")[-2] if result.key else "provider"
                    self.add_warning(
                        WarningMessage(
                            level=level,
                            category=WarningCategory.CONFIGURATION,
                            message=f"API key for {provider} is not configured",
                            details=f"Please set the API key using 'vaahai config set llm.{provider}.api_key YOUR_API_KEY' command.",
                            fix_command=f"vaahai config set llm.{provider}.api_key YOUR_API_KEY",
                            docs_url=f"https://docs.vaahai.io/configuration/{provider}",
                        )
                    )
                elif "model" in result.message.lower():
                    provider = result.key.split(".")[-2] if result.key else "provider"
                    self.add_warning(
                        WarningMessage(
                            level=level,
                            category=WarningCategory.CONFIGURATION,
                            message=f"Model for {provider} is not configured",
                            details=f"Please set the model using 'vaahai model set {provider} MODEL_NAME' command.",
                            fix_command=f"vaahai model set {provider} MODEL_NAME",
                            docs_url=f"https://docs.vaahai.io/models/{provider}",
                        )
                    )
                else:
                    # Generic warning for other validation issues
                    self.add_warning(
                        WarningMessage(
                            level=level,
                            category=WarningCategory.CONFIGURATION,
                            message=result.message,
                            fix_command="vaahai config init" if level == WarningLevel.ERROR else None,
                        )
                    )
    
    def display_warnings(
        self,
        categories: Optional[List[WarningCategory]] = None,
        min_level: WarningLevel = WarningLevel.WARNING,
        command_context: Optional[str] = None,
    ) -> bool:
        """
        Display collected warnings to the user.
        
        Args:
            categories (Optional[List[WarningCategory]]): Only show warnings in these categories
            min_level (WarningLevel): Only show warnings at or above this level
            command_context (Optional[str]): Command context for filtering warnings
            
        Returns:
            bool: True if any warnings were displayed, False otherwise
        """
        if self.quiet or not self.warnings:
            return False
        
        # Filter warnings by category and level
        filtered_warnings = self.warnings
        if categories:
            filtered_warnings = [w for w in filtered_warnings if w.category in categories]
        
        # Filter by minimum level
        level_values = {
            WarningLevel.ERROR: 3,
            WarningLevel.WARNING: 2,
            WarningLevel.INFO: 1,
        }
        min_level_value = level_values[min_level]
        filtered_warnings = [
            w for w in filtered_warnings 
            if level_values[w.level] >= min_level_value
        ]
        
        if not filtered_warnings:
            return False
        
        # Group warnings by level
        errors = [w for w in filtered_warnings if w.level == WarningLevel.ERROR]
        warnings = [w for w in filtered_warnings if w.level == WarningLevel.WARNING]
        infos = [w for w in filtered_warnings if w.level == WarningLevel.INFO]
        
        # Display header if we have warnings to show
        if errors or warnings or infos:
            if command_context:
                console.print(f"\n[bold yellow]Warnings for '{command_context}':[/bold yellow]")
            else:
                console.print("\n[bold yellow]Warning Messages:[/bold yellow]")
        
        # Display errors first
        for warning in errors:
            # Only show each warning once
            warning_key = f"{warning.level.value}:{warning.category.value}:{warning.message}"
            if warning_key in self.shown_warnings:
                continue
            
            console.print(warning.get_rich_panel())
            self.shown_warnings[warning_key] = True
        
        # Then display warnings
        for warning in warnings:
            warning_key = f"{warning.level.value}:{warning.category.value}:{warning.message}"
            if warning_key in self.shown_warnings:
                continue
            
            console.print(warning.get_rich_panel())
            self.shown_warnings[warning_key] = True
        
        # Finally display infos
        for warning in infos:
            warning_key = f"{warning.level.value}:{warning.category.value}:{warning.message}"
            if warning_key in self.shown_warnings:
                continue
            
            console.print(warning.get_rich_panel())
            self.shown_warnings[warning_key] = True
        
        return bool(errors or warnings or infos)
    
    def clear_warnings(self) -> None:
        """Clear all warnings from the system."""
        self.warnings = []
        self.shown_warnings = {}


# Create a global instance of the warning system
warning_system = WarningSystem()


def check_and_display_warnings(
    command_name: str,
    categories: Optional[List[WarningCategory]] = None,
    min_level: WarningLevel = WarningLevel.WARNING,
    quiet: bool = False,
) -> bool:
    """
    Check for warnings relevant to a command and display them.
    
    This is a convenience function for use in CLI commands.
    
    Args:
        command_name (str): Name of the command for context
        categories (Optional[List[WarningCategory]]): Categories to check
        min_level (WarningLevel): Minimum warning level to display
        quiet (bool): Whether to suppress warnings
        
    Returns:
        bool: True if any warnings were displayed, False otherwise
    """
    # Skip if quiet mode is enabled
    if quiet:
        return False
    
    # Skip for config commands to avoid circular warnings
    if command_name.startswith("config"):
        return False
    
    # Create a new warning system for this check
    system = WarningSystem(quiet=quiet)
    
    # Add configuration warnings
    system.add_config_warnings()
    
    # Display warnings
    return system.display_warnings(
        categories=categories,
        min_level=min_level,
        command_context=command_name,
    )
