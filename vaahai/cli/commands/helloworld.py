"""
Hello World CLI Command

A simple command to test the Autogen integration.
"""

import typer
from typing import Optional
from rich.console import Console
from vaahai.core.agents.factory import AgentFactory

# Create console for rich output
console = Console()

# Create the Typer application
app = typer.Typer(help="Run a simple Hello World agent to test the Autogen integration")


@app.callback(invoke_without_command=True)
def main(
    message: Optional[str] = typer.Option(
        None, "--message", "-m", help="Custom hello world message"
    ),
):
    """
    Run a simple Hello World agent to test the Autogen integration.
    
    This command creates and runs a basic HelloWorldAgent to validate
    the Autogen integration framework.
    """
    try:
        # Create configuration
        config = {}
        if message:
            config["message"] = message
        
        # Create and run the agent
        agent = AgentFactory.create_agent("hello_world", config)
        result = agent.run()
        
        # Print the result with rich formatting
        console.print(f"[bold green]Agent Response:[/bold green] {result['message']}")
        
        return result
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
