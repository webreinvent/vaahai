"""
VaahAI config validate command implementation.

This module contains the implementation of the config validate command,
which is used to validate VaahAI configuration settings.
"""

import typer
from typing import Optional, List
from pathlib import Path

from vaahai.cli.utils.console import (
    print_error,
    print_info,
    print_panel,
    print_success,
    print_warning,
    format_key,
    format_value,
)
from vaahai.cli.utils.help import CustomHelpCommand
from vaahai.config.validation import (
    validate_configuration_exists,
    validate_configuration_complete,
    validate_for_command,
    get_validation_summary
)
from vaahai.config.manager import ConfigManager


def validate_command(
    ctx: typer.Context,
    command: Optional[str] = typer.Option(
        None,
        "--command",
        "-c",
        help="Validate configuration for a specific command",
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        "-f",
        help="Attempt to fix configuration issues",
    ),
):
    """
    Validate VaahAI configuration settings.

    This command validates your VaahAI configuration settings to ensure they are
    complete and correctly set up for using VaahAI commands.
    """
    # Access global options
    verbose = (
        ctx.parent.parent.obj.get("verbose", False)
        if ctx.parent and ctx.parent.obj
        else False
    )
    quiet = (
        ctx.parent.parent.obj.get("quiet", False)
        if ctx.parent and ctx.parent.obj
        else False
    )

    # Check if configuration exists
    exists, message = validate_configuration_exists()
    if not exists:
        print_error(message)
        print_info("Run 'vaahai config init' to create a configuration file")
        if fix:
            print_info("Attempting to fix by running config init...")
            ctx.parent.invoke(ctx.parent.commands["init"])
            # Check if init fixed the issue
            exists, _ = validate_configuration_exists()
            if exists:
                print_success("Configuration created successfully!")
            else:
                print_error("Failed to create configuration!")
                raise typer.Exit(code=1)
        else:
            raise typer.Exit(code=1)

    # If validating for a specific command
    if command:
        print_panel(
            f"[bold blue]Validating Configuration for '{command}' Command[/bold blue]",
            title="Configuration Validation",
            style="blue",
        )
        
        is_valid, errors = validate_for_command(command)
        
        if is_valid:
            print_success(f"Configuration is valid for '{command}' command!")
            return
        else:
            print_error(f"Configuration is not valid for '{command}' command:")
            for error in errors:
                print_warning(f"- {error}")
            
            if fix:
                print_info("Attempting to fix configuration issues...")
                # For now, just suggest running config init
                print_info("Please run 'vaahai config init' to fix configuration issues")
            
            raise typer.Exit(code=1)
    
    # General validation
    print_panel(
        "[bold blue]Validating VaahAI Configuration[/bold blue]",
        title="Configuration Validation",
        style="blue",
    )
    
    errors = validate_configuration_complete()
    
    if not errors:
        print_success("Configuration is valid!")
        
        # Show summary of configuration
        if not quiet:
            try:
                config_manager = ConfigManager()
                provider = config_manager.get_current_provider()
                model = config_manager.get_model(provider)
                
                print_info("\n[bold]Configuration Summary:[/bold]")
                print_info(f"Provider: {provider}")
                print_info(f"Model: {model}")
                
                # Show API key status (masked)
                api_key = config_manager.get_api_key(provider)
                key_status = "Set" if api_key else "Not set"
                print_info(f"API Key: {key_status}")
                
                # Show Docker status
                docker_enabled = config_manager.get("docker.enabled", False)
                print_info(f"Docker: {'Enabled' if docker_enabled else 'Disabled'}")
            except Exception as e:
                if verbose:
                    print_warning(f"Error showing configuration summary: {str(e)}")
    else:
        print_error("Configuration is not valid:")
        for error in errors:
            print_warning(f"- {error}")
        
        if fix:
            print_info("Attempting to fix configuration issues...")
            # For now, just run config init
            ctx.parent.invoke(ctx.parent.commands["init"])
            
            # Check if init fixed all issues
            new_errors = validate_configuration_complete()
            if not new_errors:
                print_success("All configuration issues fixed!")
            else:
                print_warning("Some configuration issues remain:")
                for error in new_errors:
                    print_warning(f"- {error}")
                print_info("Please address these issues manually")
                raise typer.Exit(code=1)
        else:
            print_info("Run 'vaahai config validate --fix' to attempt to fix issues")
            raise typer.Exit(code=1)
