"""
Interactive diff report generator for code review results.

This module provides utilities for generating interactive terminal-based
reports from code review results with syntax highlighting and diff display.
"""

from typing import Any, Dict, List, Optional, Tuple
import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich import box
from rich.prompt import Prompt

from vaahai.reporting.formats import OutputFormat


class InteractiveDiffReporter:
    """
    Generates interactive terminal-based reports from code review results.
    
    This class converts the review results into an interactive Rich-based
    display showing original and suggested code with differences highlighted,
    allowing users to navigate through issues and files directly in the terminal.
    """
    
    # Severity emoji mappings
    SEVERITY_EMOJIS = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
        "info": "🔵",
    }
    
    def __init__(self, results: Dict[str, Any], console: Optional[Console] = None):
        """
        Initialize the interactive diff reporter.
        
        Args:
            results: Dictionary containing the review results
            console: Optional Rich console instance to use for output
        """
        self.results = results
        self.console = console or Console()
        self.current_issue_index = 0
        self.current_file_index = 0
        self.issues = []
        self.files = []
        self._extract_issues_and_files()
        
    def _extract_issues_and_files(self) -> None:
        """Extract all issues and files from the results for navigation."""
        if self.results.get("status") != "success":
            return
            
        # Process results based on their structure
        if "results" in self.results and isinstance(self.results["results"], dict):
            # Dictionary format
            step_results = self.results["results"]
            for step_id, step_result in step_results.items():
                for issue in step_result.get("issues", []):
                    self.issues.append({
                        "step_id": step_id,
                        "issue": issue
                    })
                    file_path = issue.get("file_path")
                    if file_path and file_path not in self.files:
                        self.files.append(file_path)
        elif "results" in self.results and isinstance(self.results["results"], list):
            # List format
            for step_result in self.results["results"]:
                step_id = step_result.get("step_id", "unknown")
                for issue in step_result.get("issues", []):
                    self.issues.append({
                        "step_id": step_id,
                        "issue": issue
                    })
                    file_path = issue.get("file_path")
                    if file_path and file_path not in self.files:
                        self.files.append(file_path)
    
    def display_interactive_report(self) -> None:
        """
        Display an interactive report from the review results.
        
        This method shows a Rich-based interactive display with navigation
        between issues and files.
        """
        if self.results.get("status") == "error":
            self._display_error_report()
            return
            
        if not self.issues:
            self.console.print("[yellow]No issues found in the review results.[/yellow]")
            return
            
        with Live(self._generate_layout(), refresh_per_second=4) as live:
            self._handle_navigation(live)
    
    def _generate_layout(self) -> Layout:
        """Generate the layout for the interactive display."""
        layout = Layout()
        
        # Create header, body, and footer sections
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Configure the body section
        layout["body"].split_row(
            Layout(name="issue_info", ratio=1),
            Layout(name="code_display", ratio=2)
        )
        
        # Fill the sections with content
        layout["header"].update(self._generate_header())
        layout["issue_info"].update(self._generate_issue_info())
        layout["code_display"].update(self._generate_code_display())
        layout["footer"].update(self._generate_footer())
        
        return layout
    
    def _generate_header(self) -> Panel:
        """Generate the header panel with report title and navigation info."""
        title = Text("VaahAI Interactive Code Review", style="bold blue")
        subtitle = Text(f"Issues: {len(self.issues)} | Files: {len(self.files)}", style="dim")
        
        return Panel(
            Columns([title, subtitle], expand=True),
            box=box.ROUNDED,
            border_style="blue"
        )
    
    def _generate_issue_info(self) -> Panel:
        """Generate the panel showing information about the current issue."""
        if not self.issues:
            return Panel("No issues found", title="Issue Details")
            
        issue_data = self.issues[self.current_issue_index]
        issue = issue_data["issue"]
        step_id = issue_data["step_id"]
        
        # Create a table for issue details
        table = Table(box=box.SIMPLE, show_header=False, expand=True)
        table.add_column("Property", style="bold")
        table.add_column("Value")
        
        # Add issue details to the table
        severity = issue.get("severity", "info").lower()
        emoji = self.SEVERITY_EMOJIS.get(severity, "")
        
        table.add_row("Step", step_id)
        table.add_row("Severity", f"{emoji} {severity.capitalize()}")
        table.add_row("File", issue.get("file_path", "N/A"))
        table.add_row("Line", str(issue.get("line_number", "N/A")))
        table.add_row("Message", issue.get("message", "N/A"))
        
        if issue.get("recommendation"):
            table.add_row("Recommendation", issue.get("recommendation"))
        
        return Panel(
            table,
            title=f"Issue {self.current_issue_index + 1}/{len(self.issues)}",
            border_style="green"
        )
    
    def _generate_code_display(self) -> Panel:
        """Generate the panel showing code with syntax highlighting and diff."""
        if not self.issues:
            return Panel("No code to display", title="Code")
            
        issue_data = self.issues[self.current_issue_index]
        issue = issue_data["issue"]
        
        file_path = issue.get("file_path")
        line_number = issue.get("line_number")
        code_snippet = issue.get("code_snippet", "")
        suggested_code = issue.get("suggested_code", "")
        
        # Determine the language for syntax highlighting
        language = "python"  # Default to Python
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in {".js", ".jsx", ".ts", ".tsx"}:
                language = "javascript"
            elif ext in {".html", ".htm"}:
                language = "html"
            elif ext in {".css"}:
                language = "css"
            elif ext in {".php"}:
                language = "php"
            elif ext in {".java"}:
                language = "java"
            elif ext in {".rb"}:
                language = "ruby"
            elif ext in {".go"}:
                language = "go"
            elif ext in {".rs"}:
                language = "rust"
            elif ext in {".c", ".cpp", ".h", ".hpp"}:
                language = "c"
            elif ext in {".md", ".markdown"}:
                language = "markdown"
            # Add more language mappings as needed
        
        # Create the code display
        if suggested_code:
            # Show side-by-side diff if we have suggested code
            original_syntax = Syntax(
                code_snippet,
                language,
                line_numbers=True,
                start_line=line_number if line_number else 1,
                theme="monokai",
                word_wrap=True
            )
            
            suggested_syntax = Syntax(
                suggested_code,
                language,
                line_numbers=True,
                start_line=line_number if line_number else 1,
                theme="monokai",
                word_wrap=True
            )
            
            columns = Columns([
                Panel(original_syntax, title="Original Code", border_style="red"),
                Panel(suggested_syntax, title="Suggested Code", border_style="green")
            ])
            
            return Panel(columns, title="Code Diff")
        else:
            # Just show the original code if no suggestion is available
            syntax = Syntax(
                code_snippet,
                language,
                line_numbers=True,
                start_line=line_number if line_number else 1,
                theme="monokai",
                word_wrap=True
            )
            
            return Panel(syntax, title=f"Code from {file_path}" if file_path else "Code")
    
    def _generate_footer(self) -> Panel:
        """Generate the footer panel with navigation instructions."""
        help_text = Text()
        help_text.append("← → : Navigate issues | ", style="dim")
        help_text.append("↑ ↓ : Navigate files | ", style="dim")
        help_text.append("q : Quit | ", style="dim")
        help_text.append("Enter : Apply suggested change", style="dim green")
        
        return Panel(
            help_text,
            box=box.ROUNDED,
            border_style="blue"
        )
    
    def _handle_navigation(self, live: Live) -> None:
        """Handle keyboard navigation in the interactive display."""
        while True:
            key = self.console.input()
            
            if key.lower() == 'q':
                break
            elif key == '\x1b[C':  # Right arrow
                self.current_issue_index = (self.current_issue_index + 1) % max(1, len(self.issues))
                live.update(self._generate_layout())
            elif key == '\x1b[D':  # Left arrow
                self.current_issue_index = (self.current_issue_index - 1) % max(1, len(self.issues))
                live.update(self._generate_layout())
            elif key == '\x1b[A':  # Up arrow
                self.current_file_index = (self.current_file_index - 1) % max(1, len(self.files))
                self._update_issue_by_file()
                live.update(self._generate_layout())
            elif key == '\x1b[B':  # Down arrow
                self.current_file_index = (self.current_file_index + 1) % max(1, len(self.files))
                self._update_issue_by_file()
                live.update(self._generate_layout())
            elif key == '\r':  # Enter
                # This would be implemented in P3-T13 (Add code change acceptance mechanism)
                self.console.print("[yellow]Code change acceptance will be implemented in a future task.[/yellow]")
    
    def _update_issue_by_file(self) -> None:
        """Update the current issue index based on the selected file."""
        if not self.files or not self.issues:
            return
            
        current_file = self.files[self.current_file_index]
        
        # Find the first issue that matches the current file
        for i, issue_data in enumerate(self.issues):
            if issue_data["issue"].get("file_path") == current_file:
                self.current_issue_index = i
                break
    
    def _display_error_report(self) -> None:
        """Display an error report."""
        error_message = self.results.get("error", "Unknown error")
        self.console.print(Panel(
            f"[bold red]Error:[/bold red] {error_message}",
            title="VaahAI Code Review Error",
            border_style="red"
        ))


def generate_interactive_diff_report(results: Dict[str, Any], console: Optional[Console] = None) -> None:
    """
    Generate and display an interactive diff report from review results.
    
    This is a helper function that creates an InteractiveDiffReporter instance
    and displays the interactive report.
    
    Args:
        results: Dictionary containing the review results
        console: Optional Rich console instance to use for output
    """
    console = console or Console()
    reporter = InteractiveDiffReporter(results, console)
    reporter.display_interactive_report()
