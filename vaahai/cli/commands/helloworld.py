"""
Hello World command implementation for VaahAI CLI.
"""
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

console = Console()

def register(app: typer.Typer):
    """
    Register the helloworld command with the Typer app.
    
    Args:
        app: The Typer app instance
    """
    @app.command("helloworld")
    def hello_world(
        name: Optional[str] = typer.Option(None, "--name", "-n", help="Your name")
    ):
        """
        Simple hello world command to demonstrate VaahAI functionality.
        """
        greeting = f"Hello, {name or 'World'}!"
        
        console.print(Panel.fit(
            f"[bold green]{greeting}[/bold green]\n\n"
            f"Welcome to [bold blue]VaahAI[/bold blue] - Your AI Agent Framework!\n\n"
            "This is a simple demonstration of the VaahAI CLI.",
            title="VaahAI Hello World",
            border_style="blue"
        ))
        
        # In the future, this will demonstrate a simple agent interaction
        console.print("\n[yellow]In the future, this command will demonstrate a simple agent interaction.[/yellow]")
