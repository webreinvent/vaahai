"""
Main CLI entry point for VaahAI.
"""
import typer
import sys
from rich.console import Console
from rich.panel import Panel

# Create Typer app instance
app = typer.Typer(
    name="vaahai",
    help="VaahAI - AI Agent Framework",
    add_completion=False,
)

# Create config command group
config_app = typer.Typer(help="Configuration commands")
app.add_typer(config_app, name="config")

console = Console()

@app.command("helloworld")
def hello_world(
    name: str = typer.Option(None, "--name", "-n", help="Your name")
):
    """
    Simple hello world command that will eventually use Autogen AI.
    """
    greeting = f"Hello, {name or 'World'}!"
    
    console.print(Panel.fit(
        f"[bold green]{greeting}[/bold green]\n\n"
        f"Welcome to [bold blue]VaahAI[/bold blue] - Your AI Agent Framework!\n\n"
        "This is a simple demonstration of the VaahAI CLI.",
        title="VaahAI Hello World",
        border_style="blue"
    ))
    
    # In the future, this will demonstrate Autogen AI agent interaction
    console.print("\n[yellow]In the future, this command will demonstrate Autogen AI agent interaction.[/yellow]")

@config_app.command("init")
def config_init(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing configuration")
):
    """
    Initialize VaahAI configuration.
    """
    console.print(Panel.fit(
        "Initializing VaahAI configuration...\n\n"
        "This will create a default configuration file in your home directory.",
        title="VaahAI Config Initialization",
        border_style="green"
    ))
    
    # This will be implemented to create actual config files
    console.print("[yellow]Config initialization will be implemented in the next step.[/yellow]")

@app.command("version")
def version():
    """
    Show VaahAI version information.
    """
    console.print(Panel.fit(
        "[bold]VaahAI[/bold] version 0.1.0\n"
        "AI Agent Framework",
        title="Version Info",
        border_style="green"
    ))

@app.callback()
def callback():
    """
    VaahAI - AI Agent Framework.
    
    A powerful framework for building, managing, and orchestrating AI agents.
    """
    pass

def main():
    """
    Main entry point for the CLI.
    """
    try:
        app()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
