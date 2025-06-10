#!/usr/bin/env python
"""
Configuration Management Example

This script demonstrates how to use the VaahAI configuration management system
programmatically, including loading, modifying, and saving configuration values.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path to allow importing vaahai
sys.path.append(str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from vaahai.config.manager import ConfigManager
from vaahai.config.llm_utils import list_providers, list_models, validate_api_key


def print_section(title):
    """Print a section title."""
    console = Console()
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print("=" * len(title))


def main():
    """Demonstrate configuration management features."""
    console = Console()
    
    # Create a ConfigManager instance
    print_section("Creating ConfigManager")
    config_manager = ConfigManager()
    console.print("ConfigManager created successfully")
    
    # Check if configuration exists
    print_section("Checking Configuration")
    if config_manager.exists():
        console.print("[green]Configuration file exists[/green]")
    else:
        console.print("[yellow]Configuration file does not exist[/yellow]")
        console.print("Creating default configuration...")
        config_manager.save(user_level=True)
        console.print("[green]Default configuration created[/green]")
    
    # Get and display the current configuration
    print_section("Current Configuration")
    config = config_manager.get_full_config()
    
    # Display current provider
    current_provider = config_manager.get_current_provider()
    console.print(f"Current LLM provider: [bold]{current_provider}[/bold]")
    
    # Display available providers
    providers = list_providers()
    console.print(f"Available providers: {', '.join(providers)}")
    
    # Display provider settings in a table
    provider_table = Table(title="Provider Settings")
    provider_table.add_column("Provider")
    provider_table.add_column("API Key")
    provider_table.add_column("Model")
    
    for provider in providers:
        api_key = config.get("providers", {}).get(provider, {}).get("api_key", "")
        model = config.get("providers", {}).get(provider, {}).get("model", "")
        
        # Mask API key for display
        masked_key = "********" if api_key else ""
        
        provider_table.add_row(
            provider,
            masked_key,
            model
        )
    
    console.print(provider_table)
    
    # Display Docker settings
    docker_enabled = config.get("docker", {}).get("enabled", False)
    docker_image = config.get("docker", {}).get("image", "")
    docker_memory = config.get("docker", {}).get("memory", "")
    
    docker_panel = Panel(
        f"Enabled: {docker_enabled}\n"
        f"Image: {docker_image or 'Not set'}\n"
        f"Memory: {docker_memory or 'Not set'}",
        title="Docker Settings"
    )
    console.print(docker_panel)
    
    # Demonstrate getting a specific config value
    print_section("Getting Specific Configuration Values")
    provider_value = config_manager.get("llm.provider")
    console.print(f"llm.provider = [bold]{provider_value}[/bold]")
    
    # Demonstrate setting a configuration value
    print_section("Setting Configuration Values")
    console.print("Setting output.color to False...")
    config_manager.set("output.color", False)
    console.print("Setting docker.enabled to True...")
    config_manager.set("docker.enabled", True)
    
    # Save the configuration (but don't actually save to avoid modifying the user's config)
    print_section("Saving Configuration (Simulated)")
    console.print("[yellow]Note: In this example, we're not actually saving the changes[/yellow]")
    # config_manager.save(user_level=True)  # Commented out to avoid modifying user's config
    
    # Demonstrate validation
    print_section("Configuration Validation")
    validation_issues = config_manager.validate()
    if validation_issues:
        console.print("[yellow]Validation issues found:[/yellow]")
        for issue in validation_issues:
            console.print(f"- {issue}")
    else:
        console.print("[green]Configuration is valid[/green]")
    
    # Demonstrate environment variable overrides
    print_section("Environment Variable Overrides")
    console.print("You can override configuration values with environment variables:")
    console.print("export VAAHAI_LLM_PROVIDER=claude")
    console.print("export VAAHAI_PROVIDERS_OPENAI_API_KEY=your-api-key")
    
    # Show an example of how this would work
    os.environ["VAAHAI_LLM_PROVIDER"] = "claude"  # Temporary for demonstration
    overridden_config = config_manager.get_full_config()
    console.print(f"With environment variable set, llm.provider = [bold]{overridden_config.get('llm', {}).get('provider')}[/bold]")
    del os.environ["VAAHAI_LLM_PROVIDER"]  # Clean up
    
    # Demonstrate model listing
    print_section("Available Models")
    try:
        # Only show models for the current provider to avoid API calls to all providers
        models = list_models(current_provider)
        console.print(f"Models for {current_provider}: {', '.join(models[:5])}...")
        console.print(f"Total models available: {len(models)}")
    except Exception as e:
        console.print(f"[yellow]Could not list models: {str(e)}[/yellow]")
    
    # Finish
    print_section("Summary")
    console.print("""
The VaahAI configuration system provides:
1. Hierarchical configuration with user and project levels
2. Environment variable overrides
3. Schema validation
4. Secure API key handling
5. Provider and model management
6. Docker configuration
    """)


if __name__ == "__main__":
    main()
