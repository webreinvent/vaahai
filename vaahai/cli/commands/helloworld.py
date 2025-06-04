"""
Hello World CLI Command

A simple command to test the Autogen integration.
"""

import typer
from typing import Optional
from rich.console import Console
from vaahai.core.agents.factory import AgentFactory
from vaahai.core.agents.base import AUTOGEN_AVAILABLE
from vaahai.core.config import config_manager

# Create console for rich output
console = Console()

# Create the Typer application
app = typer.Typer(help="Run a simple Hello World agent to test the Autogen integration")


@app.callback(invoke_without_command=True)
def main(
    message: Optional[str] = typer.Option(
        None, "--message", "-m", help="Custom hello world message"
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", help="OpenAI API key for Autogen integration (overrides global config)"
    ),
    model: Optional[str] = typer.Option(
        None, "--model", help="Model to use for Autogen (overrides global config)"
    ),
    temperature: Optional[float] = typer.Option(
        None, "--temperature", help="Temperature for model generation (overrides global config)"
    ),
    save_config: bool = typer.Option(
        False, "--save-config", "-s", help="Save provided parameters to global configuration"
    ),
):
    """
    Run a simple Hello World agent to test the Autogen integration.
    
    This command creates and runs a basic HelloWorldAgent to validate
    the Autogen integration framework.
    """
    try:
        # Check if Autogen is available
        if not AUTOGEN_AVAILABLE:
            console.print("[bold red]Warning:[/] Autogen dependencies are not fully available.")
            console.print("Some features may be limited. To use full functionality, install the required dependencies:")
            console.print("  [bold]pip install flaml[automl] xgboost[/]")
            console.print("On macOS, you may also need to install OpenMP: [bold]brew install libomp[/]")
            console.print("\nContinuing with limited functionality...\n")
            
        # Create configuration
        config = {}
        if message:
            config["message"] = message
        if api_key:
            config["api_key"] = api_key
        if model:
            config["model"] = model
        if temperature is not None:
            config["temperature"] = temperature
        
        # Save to global config if requested
        if save_config:
            if api_key:
                config_manager.set("llm.api_key", api_key, save=True)
                console.print("[bold green]Saved API key to global configuration[/bold green]")
            if model:
                config_manager.set("autogen.default_model", model, save=True)
                console.print(f"[bold green]Saved model '{model}' to global configuration[/bold green]")
            if temperature is not None:
                config_manager.set("autogen.temperature", temperature, save=True)
                console.print(f"[bold green]Saved temperature {temperature} to global configuration[/bold green]")
        
        # Create and run the agent
        agent = AgentFactory.create_agent("hello_world", config)
        result = agent.run()
        
        # Print the result with rich formatting
        if "warning" in result and result["warning"] == "missing_api_key":
            # Special formatting for warning messages
            console.print(result["message"])
        else:
            console.print(f"[bold green]Agent Response:[/bold green] {result['message']}")
        
        return result
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
