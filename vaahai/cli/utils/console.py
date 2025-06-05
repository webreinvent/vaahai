"""
Console output utilities for VaahAI CLI.

This module provides utility functions for consistent console output formatting
using Rich library across all CLI commands.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from typing import Optional, List, Dict, Any, Union

# Create a shared console instance for consistent styling
console = Console()


def print_header(title: str, subtitle: Optional[str] = None) -> None:
    """
    Print a formatted header with optional subtitle.
    
    Args:
        title: The main title text
        subtitle: Optional subtitle text
    """
    console.print(f"[bold blue]{title}[/bold blue]")
    if subtitle:
        console.print(f"[dim]{subtitle}[/dim]")
    console.print("")


def print_success(message: str) -> None:
    """
    Print a success message.
    
    Args:
        message: The success message to print
    """
    console.print(f"[bold green]✓ {message}[/bold green]")


def print_error(message: str) -> None:
    """
    Print an error message.
    
    Args:
        message: The error message to print
    """
    console.print(f"[bold red]✗ {message}[/bold red]")


def print_warning(message: str) -> None:
    """
    Print a warning message.
    
    Args:
        message: The warning message to print
    """
    console.print(f"[bold yellow]⚠ {message}[/bold yellow]")


def print_info(message: str) -> None:
    """
    Print an info message.
    
    Args:
        message: The info message to print
    """
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")


def print_panel(
    content: str,
    title: Optional[str] = None,
    style: str = "blue",
    expand: bool = True,
) -> None:
    """
    Print content in a panel with optional title.
    
    Args:
        content: The content to display in the panel
        title: Optional title for the panel
        style: Color style for the panel border
        expand: Whether to expand the panel to fill the terminal width
    """
    panel = Panel(
        content,
        title=title,
        border_style=style,
        expand=expand,
    )
    console.print(panel)


def print_code(
    code: str,
    language: str = "python",
    line_numbers: bool = True,
    title: Optional[str] = None,
) -> None:
    """
    Print formatted code with syntax highlighting.
    
    Args:
        code: The code to print
        language: The programming language for syntax highlighting
        line_numbers: Whether to show line numbers
        title: Optional title for the code block
    """
    syntax = Syntax(
        code,
        language,
        line_numbers=line_numbers,
        theme="monokai",
    )
    if title:
        console.print(f"[bold]{title}[/bold]")
    console.print(syntax)


def print_markdown(markdown_text: str) -> None:
    """
    Print formatted markdown text.
    
    Args:
        markdown_text: The markdown text to print
    """
    md = Markdown(markdown_text)
    console.print(md)


def create_table(
    columns: List[str],
    rows: List[List[Any]],
    title: Optional[str] = None,
) -> Table:
    """
    Create a formatted table.
    
    Args:
        columns: List of column headers
        rows: List of rows, each containing values for each column
        title: Optional title for the table
        
    Returns:
        A Rich Table object that can be printed with console.print()
    """
    table = Table(title=title)
    
    # Add columns
    for column in columns:
        table.add_column(column)
    
    # Add rows
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    
    return table
