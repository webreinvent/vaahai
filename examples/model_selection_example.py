#!/usr/bin/env python3
"""
Model Selection Example for VaahAI

This example demonstrates how to use the model selection functionality in VaahAI,
including listing models, filtering by capabilities, getting model information,
and setting models for different providers.
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vaahai.config.manager import ConfigManager
from vaahai.config.llm_utils import (
    list_providers,
    list_models,
    get_all_capabilities,
    get_providers_with_capability,
    filter_models_by_capability,
    filter_models_by_capabilities,
    filter_models_by_context_length,
    get_model_info,
)

# Create a rich console for formatted output
console = Console()


def print_section(title):
    """Print a section title."""
    console.print(f"\n[bold cyan]== {title} ==[/bold cyan]")


def main():
    """Run the model selection example."""
    # Create a ConfigManager instance
    config_manager = ConfigManager()
    
    print_section("Current Configuration")
    current_provider = config_manager.get_current_provider()
    current_model = config_manager.get_model()
    console.print(f"Current provider: [bold green]{current_provider}[/bold green]")
    console.print(f"Current model: [bold green]{current_model}[/bold green]")
    
    # Get model information
    model_info = config_manager.get_model_info()
    console.print(Panel(
        f"Model: [bold]{model_info['name']}[/bold]\n"
        f"Provider: {model_info['provider']}\n"
        f"Capabilities: {', '.join(model_info['capabilities'])}\n"
        f"Context Length: {model_info['context_length']:,} tokens\n"
        f"Description: {model_info['description']}",
        title="Current Model Information",
        expand=False
    ))
    
    # List all available providers
    print_section("Available Providers")
    providers = list_providers()
    for provider in providers:
        console.print(f"- {provider}")
    
    # List models for each provider
    print_section("Available Models by Provider")
    for provider in providers:
        console.print(f"\n[bold]{provider.upper()}[/bold] models:")
        models = list_models(provider)
        for model in models:
            console.print(f"- {model}")
    
    # List available capabilities
    print_section("Available Model Capabilities")
    capabilities = get_all_capabilities()
    
    # Create a table for capabilities
    table = Table(title="Model Capabilities")
    table.add_column("Capability", style="cyan")
    table.add_column("Description", style="blue")
    table.add_column("Providers", style="green")
    
    # Add rows for each capability
    for cap in capabilities:
        # Get providers with the capability
        providers_with_cap = get_providers_with_capability(cap)
        providers_str = ", ".join(providers_with_cap) if providers_with_cap else "None"
        
        # Get description based on capability
        if cap == "text":
            description = "Basic text generation and understanding"
        elif cap == "code":
            description = "Code generation and understanding"
        elif cap == "vision":
            description = "Image understanding and processing"
        elif cap == "audio":
            description = "Audio transcription and understanding"
        elif cap == "embedding":
            description = "Vector embedding generation"
        elif cap == "function_calling":
            description = "Structured function calling capabilities"
        else:
            description = ""
        
        table.add_row(cap, description, providers_str)
    
    # Print the table
    console.print(table)
    
    # Filter models by capability
    print_section("Models with Vision Capability")
    for provider in providers:
        vision_models = filter_models_by_capability(provider, "vision")
        if vision_models:
            console.print(f"\n[bold]{provider.upper()}[/bold] models with vision capability:")
            for model in vision_models:
                console.print(f"- {model}")
    
    # Filter models by multiple capabilities
    print_section("Models with Both Vision and Function Calling Capabilities")
    for provider in providers:
        advanced_models = filter_models_by_capabilities(provider, ["vision", "function_calling"])
        if advanced_models:
            console.print(f"\n[bold]{provider.upper()}[/bold] models with vision and function calling:")
            for model in advanced_models:
                console.print(f"- {model}")
    
    # Filter models by context length
    print_section("Models with Large Context Windows (>= 100K tokens)")
    for provider in providers:
        large_context_models = filter_models_by_context_length(provider, 100000)
        if large_context_models:
            console.print(f"\n[bold]{provider.upper()}[/bold] models with context length >= 100K tokens:")
            for model in large_context_models:
                model_info = get_model_info(provider, model)
                console.print(f"- {model} ({model_info[2]:,} tokens)")
    
    # Get recommended models
    print_section("Recommended Models by Capability")
    
    # For code generation
    try:
        code_model = config_manager.get_recommended_model(["code"])
        console.print(f"Recommended model for code generation: [bold green]{code_model}[/bold green]")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    # For vision tasks
    try:
        vision_model = config_manager.get_recommended_model(["vision"])
        console.print(f"Recommended model for vision tasks: [bold green]{vision_model}[/bold green]")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    # For advanced tasks requiring multiple capabilities
    try:
        advanced_model = config_manager.get_recommended_model(["code", "vision", "function_calling"])
        console.print(f"Recommended model for advanced tasks: [bold green]{advanced_model}[/bold green]")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    # Demonstrate setting a model
    print_section("Setting a Different Model")
    
    # Save the original model to restore later
    original_provider = config_manager.get_current_provider()
    original_model = config_manager.get_model()
    
    # Set a new model for the current provider
    try:
        # Get the first available model that's different from the current one
        provider = config_manager.get_current_provider()
        models = list_models(provider)
        new_model = next((m for m in models if m != original_model), None)
        
        if new_model:
            console.print(f"Setting model to: [bold green]{new_model}[/bold green]")
            config_manager.set_model(new_model)
            console.print(f"Model set successfully (not saved to config)")
            
            # Get the new model information
            model_info = config_manager.get_model_info()
            console.print(Panel(
                f"Model: [bold]{model_info['name']}[/bold]\n"
                f"Provider: {model_info['provider']}\n"
                f"Capabilities: {', '.join(model_info['capabilities'])}\n"
                f"Context Length: {model_info['context_length']:,} tokens\n"
                f"Description: {model_info['description']}",
                title="New Model Information",
                expand=False
            ))
            
            # Restore the original model
            config_manager.set_model(original_model)
            console.print(f"Restored original model: [bold green]{original_model}[/bold green]")
        else:
            console.print("[bold yellow]No alternative model available for demonstration[/bold yellow]")
    
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
    
    print_section("Example Complete")
    console.print("This example demonstrated the model selection functionality in VaahAI.")
    console.print("Use the 'vaahai model' command in the CLI for interactive model management.")


if __name__ == "__main__":
    main()
