"""
VaahAI review command implementation.

This module contains the implementation of the review command,
which is used to perform code reviews on files or directories.
"""

import os
import logging
import time
import threading
from pathlib import Path
from typing import List, Optional
import sys
from datetime import datetime

import typer
from InquirerPy import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table

from vaahai.cli.utils.help import CustomHelpCommand, create_typer_app
from vaahai.review.steps.registry import ReviewStepRegistry
from vaahai.review.runner import ReviewRunner
from vaahai.review.steps.base import ReviewStep, ReviewStepCategory, ReviewStepSeverity
from vaahai.review.steps.progress import ReviewStepStatus
from vaahai.reporting.formats import OutputFormat
from vaahai.reporting.markdown_reporter import generate_markdown_report
from vaahai.reporting.html_reporter import generate_html_report

# Import built-in review steps to ensure they are registered
from vaahai.review.steps.built_in import LineLength, IndentationConsistency
from vaahai.review.steps.built_in import HardcodedSecrets, SQLInjection
from vaahai.review.steps.built_in import InefficientLoops, LargeMemoryUsage

# Create a rich console for formatted output
console = Console()

# Create the review command group with custom help formatting
review_app = create_typer_app(
    name="review",
    help="Perform code reviews on files or directories",
    add_completion=False,
)


@review_app.callback()
def callback():
    """
    Perform code reviews on files or directories.
    """
    pass


@review_app.command("run", cls=CustomHelpCommand)
def run(
    path: Path = typer.Argument(
        ...,
        help="Path to the file or directory to review",
        exists=True,
    ),
    depth: str = typer.Option(
        "standard",
        "--depth",
        "-d",
        help="Depth of the review (quick, standard, thorough)",
    ),
    focus: Optional[str] = typer.Option(
        None,
        "--focus",
        "-f",
        help="Focus area for the review (style, security, performance)",
    ),
    severity: Optional[str] = typer.Option(
        None,
        "--severity",
        "-s",
        help="Minimum severity level (critical, high, medium, low)",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Show debug information",
    ),
    format: str = typer.Option(
        None,
        "--format",
        "-f",
        help="Output format for the report (rich, markdown, html, interactive)",
        case_sensitive=False,
    ),
):
    """
    Run a code review on the specified file or directory.

    This command analyzes the code in the specified path and provides
    feedback on code quality, potential bugs, and suggested improvements.
    """
    # Enable debug logging if debug flag is set
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("vaahai.review").setLevel(logging.DEBUG)
    
    console.print(
        Panel(
            f"[bold]Reviewing:[/bold] {path}\n"
            f"[bold]Depth:[/bold] {depth}\n"
            f"[bold]Focus:[/bold] {focus or 'All areas'}\n"
            f"[bold]Severity:[/bold] {severity or 'All levels'}",
            title="Code Review",
            border_style="blue",
        )
    )

    # Debug: Check if review steps are registered
    registry = ReviewStepRegistry()
    all_steps = registry.get_all_steps()
    if debug:
        console.print(f"[bold]Debug:[/bold] Found {len(all_steps)} registered review step classes:")
        for step_id, step_class in all_steps.items():
            # Check if the class has severity attribute
            severity_value = getattr(step_class, "severity", None)
            console.print(f"  - {step_id}: {step_class.__name__} (Severity: {severity_value})")

    # Convert focus string to category enum if provided
    category = None
    if focus:
        try:
            category = ReviewStepCategory[focus.upper()]
            if debug:
                console.print(f"[bold]Debug:[/bold] Selected category: {category.name} ({category.value})")
        except KeyError:
            console.print(f"[yellow]Warning:[/yellow] Unknown focus area '{focus}'. Using all areas.")
    
    # Convert severity string to severity enum if provided
    min_severity = None
    if severity:
        try:
            min_severity = ReviewStepSeverity[severity.upper()]
        except KeyError:
            console.print(f"[yellow]Warning:[/yellow] Unknown severity level '{severity}'. Using all levels.")
    
    # Determine severity level based on depth
    if depth == "quick":
        # For quick reviews, use only critical and high severity steps
        min_severity_level = ReviewStepSeverity.HIGH
    elif depth == "thorough":
        # For thorough reviews, use all steps
        min_severity_level = ReviewStepSeverity.LOW
    else:  # standard
        # For standard reviews, exclude low severity steps
        min_severity_level = ReviewStepSeverity.MEDIUM
        
    # Override with user-specified severity if provided
    if min_severity:
        min_severity_level = min_severity
    
    # Create a mapping of severity levels to their ordinal values for comparison
    # Higher severity has lower ordinal value (CRITICAL=0, HIGH=1, etc.)
    severity_order = {
        ReviewStepSeverity.CRITICAL: 0,
        ReviewStepSeverity.HIGH: 1,
        ReviewStepSeverity.MEDIUM: 2,
        ReviewStepSeverity.LOW: 3
    }
    
    min_severity_ordinal = severity_order.get(min_severity_level, 3)
    
    if debug:
        console.print(f"[bold]Debug:[/bold] Minimum severity level: {min_severity_level.name} (ordinal: {min_severity_ordinal})")
    
    # If format not provided, ask with InquirerPy
    if format is None:
        # Skip prompt in non-interactive environments (e.g., during tests)
        if not hasattr(sys.stdin, "isatty") or not sys.stdin.isatty():
            format = OutputFormat.RICH.value
        else:
            format = inquirer.select(
                message="Select output format",
                choices=[
                    ("Rich (default colourful CLI)", OutputFormat.RICH.value),
                    ("Markdown", OutputFormat.MARKDOWN.value),
                    ("HTML", OutputFormat.HTML.value),
                    ("Interactive Rich diff", OutputFormat.INTERACTIVE.value),
                ],
                default=OutputFormat.RICH.value,
            ).execute()
            # If a tuple is returned (edge case), extract value
            if isinstance(format, tuple):
                format = format[1]
    
    # Validate format string to enum (fallback to RICH)
    try:
        output_format = OutputFormat(format.lower())
    except ValueError:
        console.print(f"[yellow]Unknown format '{format}', falling back to 'rich'.[/yellow]")
        output_format = OutputFormat.RICH
    
    # Use a single Progress context manager for all progress reporting
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        # Initialize step instances
        init_task = progress.add_task("Creating review step instances...", total=1)
        
        # Create instances of all review steps
        step_instances = []
        for step_id in all_steps:
            instance = registry.create_step_instance(step_id)
            if instance:
                step_instances.append(instance)
        
        progress.update(init_task, completed=1, description=f"Created {len(step_instances)} review step instances")
        
        # Debug: Show all step instances with their categories and severities
        if debug:
            console.print("\n[bold]Debug:[/bold] All step instances:")
            for step in step_instances:
                step_severity_ordinal = severity_order.get(step.severity, 3)
                console.print(f"  - {step.id}: {step.__class__.__name__} (Category: {step.category.name} ({step.category.value}), Severity: {step.severity.name} (ordinal: {step_severity_ordinal}))")
        
        # Filter step instances based on category and severity
        filter_task = progress.add_task("Filtering review steps...", total=1)
        
        filtered_instances = []
        for step in step_instances:
            # Filter by category if specified
            if category and step.category != category:
                if debug:
                    console.print(f"  - [red]✗[/red] {step.id}: Filtered out due to category mismatch (step: {step.category.name}, filter: {category.name})")
                continue
                
            # Filter by severity based on depth
            step_severity_ordinal = severity_order.get(step.severity, 3)
            if step_severity_ordinal <= min_severity_ordinal:
                filtered_instances.append(step)
                if debug:
                    console.print(f"  - [green]✓[/green] {step.id}: Included in filtered steps")
            else:
                if debug:
                    console.print(f"  - [red]✗[/red] {step.id}: Filtered out due to severity (step: {step.severity.name} (ordinal: {step_severity_ordinal}), min: {min_severity_level.name} (ordinal: {min_severity_ordinal}))")
        
        progress.update(filter_task, completed=1, description=f"Selected {len(filtered_instances)} review steps")
        
        # Debug: Show which steps will be run
        if debug and filtered_instances:
            console.print("\n[bold]Debug:[/bold] Steps that will be run:")
            for step in filtered_instances:
                console.print(f"  - {step.id}: {step.__class__.__name__} (Category: {step.category.name}, Severity: {step.severity.name})")
        elif debug and not filtered_instances:
            console.print("\n[bold red]Debug:[/bold red] No steps will be run after filtering.")
        
        # Create a ReviewRunner with the filtered instances
        runner = ReviewRunner(steps=filtered_instances)
        
        # Create a progress display for the review steps
        if filtered_instances:
            # Add a task for overall progress
            overall_task = progress.add_task(
                "Running review steps...", 
                total=len(filtered_instances)
            )
            
            # Add tasks for each review step
            step_tasks = {}
            for step in filtered_instances:
                step_tasks[step.id] = progress.add_task(
                    f"[cyan]{step.id}[/cyan] ({step.category.name})",
                    total=1,
                    visible=False
                )
            
            # Run the review with progress tracking
            try:
                # Start a background thread to update progress
                def update_progress():
                    completed_steps = 0
                    
                    while completed_steps < len(filtered_instances):
                        # Get current progress
                        progress_info = runner.get_progress().get_progress_summary()
                        
                        # Update overall progress
                        completed_steps = (
                            progress_info["completed_steps"] + 
                            progress_info["failed_steps"] + 
                            progress_info["skipped_steps"]
                        )
                        progress.update(overall_task, completed=completed_steps)
                        
                        # Update individual step progress
                        for step_id, status in runner.get_progress().step_statuses.items():
                            if step_id in step_tasks:
                                # Make the task visible if it's in progress
                                if status == ReviewStepStatus.IN_PROGRESS:
                                    progress.update(step_tasks[step_id], visible=True)
                                
                                # Update completion status
                                if status in [ReviewStepStatus.COMPLETED, ReviewStepStatus.FAILED]:
                                    progress.update(
                                        step_tasks[step_id], 
                                        completed=1,
                                        visible=True,
                                        description=(
                                            f"[green]{step_id}[/green] ({runner.get_progress().get_step_duration(step_id):.2f}s)"
                                            if status == ReviewStepStatus.COMPLETED
                                            else f"[red]{step_id}[/red] (failed)"
                                        )
                                    )
                        
                        # Sleep briefly to avoid high CPU usage
                        time.sleep(0.1)
                        
                        # Exit if all steps are completed
                        if completed_steps >= len(filtered_instances):
                            break
                
                # Start the progress update in a separate thread
                progress_thread = threading.Thread(target=update_progress)
                progress_thread.daemon = True
                progress_thread.start()
                
                # Run the review
                if path.is_file():
                    # Run on a single file
                    with open(path, 'r') as f:
                        content = f.read()
                    result = runner.run_on_content(content, file_path=str(path), output_format=output_format)
                else:
                    # Run on a directory
                    result = runner.run_on_directory(str(path), output_format=output_format)
                
                # Wait for the progress thread to catch up
                time.sleep(0.5)
                
                # Handle different output formats
                if output_format == OutputFormat.MARKDOWN:
                    # Generate markdown report
                    markdown_report = generate_markdown_report(result)
                    
                    # Create a report file with timestamp
                    report_path = f"vaahai_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                    with open(report_path, "w") as f:
                        f.write(markdown_report)
                    
                    console.print(f"\n[green]Markdown report generated:[/green] {report_path}")
                    
                    # Show a preview of the report
                    preview_length = min(500, len(markdown_report))
                    console.print("\n[bold]Report Preview:[/bold]")
                    console.print(Panel(
                        markdown_report[:preview_length] + ("..." if len(markdown_report) > preview_length else ""),
                        title="Markdown Preview",
                        border_style="blue"
                    ))
                    
                    # Return early as we've already handled the output
                    console.print(f"[green]Report format:[/green] {output_format.value}")
                    return report_path
                
                elif output_format == OutputFormat.HTML:
                    # Generate HTML report
                    html_report = generate_html_report(result)
                    
                    # Create a report file with timestamp
                    report_path = f"vaahai_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                    with open(report_path, "w") as f:
                        f.write(html_report)
                    
                    console.print(f"\n[green]HTML report generated:[/green] {report_path}")
                    
                    # Show a preview of the report
                    preview_length = min(500, len(html_report))
                    console.print("\n[bold]Report Preview:[/bold]")
                    console.print(Panel(
                        html_report[:preview_length] + ("..." if len(html_report) > preview_length else ""),
                        title="HTML Preview",
                        border_style="blue"
                    ))
                    
                    # Return early as we've already handled the output
                    console.print(f"[green]Report format:[/green] {output_format.value}")
                    return report_path
                
                # Display results
                if result["status"] == "success":
                    total_issues = 0
                    step_results = {}
                    
                    # Process results based on their structure
                    if "results" in result and isinstance(result["results"], dict):
                        # Dictionary format
                        step_results = result["results"]
                        for step_result in step_results.values():
                            total_issues += len(step_result.get("issues", []))
                    elif "results" in result and isinstance(result["results"], list):
                        # List format
                        for step_result in result["results"]:
                            step_id = step_result.get("step_id")
                            if step_id:
                                step_results[step_id] = step_result
                                total_issues += len(step_result.get("issues", []))
                    
                    # Display progress summary
                    progress_summary = result.get("progress", {})
                    if progress_summary:
                        console.print("\n[bold]Review Progress Summary:[/bold]")
                        console.print(f"Total steps: {progress_summary.get('total_steps', 0)}")
                        console.print(f"Completed steps: {progress_summary.get('completed_steps', 0)}")
                        console.print(f"Failed steps: {progress_summary.get('failed_steps', 0)}")
                        console.print(f"Skipped steps: {progress_summary.get('skipped_steps', 0)}")
                        console.print(f"Total duration: {progress_summary.get('total_duration', 0):.2f} seconds")
                    
                    # Display statistics summary
                    statistics_summary = result.get("statistics", {})
                    if statistics_summary:
                        console.print("\n[bold]Review Statistics Summary:[/bold]")
                        
                        # File statistics
                        total_files = statistics_summary.get("total_files", 0)
                        files_with_issues = statistics_summary.get("files_with_issues", 0)
                        files_with_issues_percentage = statistics_summary.get("files_with_issues_percentage", 0)
                        
                        console.print(f"Files reviewed: {total_files}")
                        console.print(f"Files with issues: {files_with_issues} ({files_with_issues_percentage:.1f}%)")
                        console.print(f"Total issues: {statistics_summary.get('total_issues', 0)}")
                        console.print(f"Average issues per file: {statistics_summary.get('issues_per_file', 0):.2f}")
                        
                        # Issues by severity
                        issues_by_severity = statistics_summary.get("issues_by_severity", {})
                        if issues_by_severity:
                            console.print("\n[bold]Issues by Severity:[/bold]")
                            severity_table = Table(show_header=True, header_style="bold")
                            severity_table.add_column("Severity", style="cyan")
                            severity_table.add_column("Count", style="yellow")
                            severity_table.add_column("Percentage", style="green")
                            
                            total_issues = statistics_summary.get("total_issues", 0)
                            for severity, count in issues_by_severity.items():
                                percentage = (count / total_issues * 100) if total_issues > 0 else 0
                                severity_style = {
                                    "critical": "bold red",
                                    "high": "red",
                                    "medium": "yellow",
                                    "low": "green",
                                    "info": "blue",
                                }.get(severity.lower(), "white")
                                
                                severity_table.add_row(
                                    f"[{severity_style}]{severity.upper()}[/{severity_style}]",
                                    str(count),
                                    f"{percentage:.1f}%"
                                )
                            
                            console.print(severity_table)
                        
                        # Issues by category
                        issues_by_category = statistics_summary.get("issues_by_category", {})
                        if issues_by_category:
                            console.print("\n[bold]Issues by Category:[/bold]")
                            category_table = Table(show_header=True, header_style="bold")
                            category_table.add_column("Category", style="cyan")
                            category_table.add_column("Count", style="yellow")
                            category_table.add_column("Percentage", style="green")
                            
                            for category, count in sorted(issues_by_category.items(), key=lambda x: x[1], reverse=True):
                                percentage = (count / total_issues * 100) if total_issues > 0 else 0
                                category_table.add_row(
                                    category.upper(),
                                    str(count),
                                    f"{percentage:.1f}%"
                                )
                            
                            console.print(category_table)
                        
                        # Most common issues
                        most_common_issues = statistics_summary.get("most_common_issues", [])
                        if most_common_issues:
                            console.print("\n[bold]Most Common Issues:[/bold]")
                            common_issues_table = Table(show_header=True, header_style="bold")
                            common_issues_table.add_column("Issue", style="cyan")
                            common_issues_table.add_column("Count", style="yellow")
                            
                            for issue, count in most_common_issues[:5]:  # Show top 5
                                common_issues_table.add_row(
                                    issue[:100] + ("..." if len(issue) > 100 else ""),  # Truncate long messages
                                    str(count)
                                )
                            
                            console.print(common_issues_table)
                    
                    # Display key findings
                    key_findings = result.get("key_findings", [])
                    if key_findings:
                        console.print("\n[bold yellow]Key Findings:[/bold yellow]")
                        findings_table = Table(show_header=True, header_style="bold")
                        findings_table.add_column("Type", style="cyan")
                        findings_table.add_column("Finding", style="yellow")
                        findings_table.add_column("Count", style="green")
                        
                        for finding in key_findings:
                            finding_type = finding.get("type", "")
                            count = finding.get("count", 0)
                            message = finding.get("message", "")
                            
                            # Determine style based on type and severity
                            if finding_type == "severity":
                                severity = finding.get("severity", "").lower()
                                type_display = f"[bold]{severity.upper()}[/bold]"
                                type_style = {
                                    "critical": "bold red",
                                    "high": "red",
                                    "medium": "yellow",
                                    "low": "green",
                                    "info": "blue",
                                }.get(severity, "white")
                                
                                findings_table.add_row(
                                    f"[{type_style}]{type_display}[/{type_style}]",
                                    message,
                                    str(count)
                                )
                            elif finding_type == "category":
                                category = finding.get("category", "").upper()
                                findings_table.add_row(
                                    f"[bold cyan]{category}[/bold cyan]",
                                    message,
                                    str(count)
                                )
                            elif finding_type == "common_issue":
                                findings_table.add_row(
                                    "COMMON",
                                    message[:100] + ("..." if len(message) > 100 else ""),
                                    str(count)
                                )
                        
                        console.print(findings_table)
                    
                    # Display recommendations
                    recommendations = result.get("recommendations", [])
                    if recommendations:
                        console.print("\n[bold green]Recommendations:[/bold green]")
                        recommendations_panel = Panel(
                            "\n".join([f"• {rec}" for rec in recommendations]),
                            title="Actionable Steps",
                            border_style="green"
                        )
                        console.print(recommendations_panel)
                    
                    if total_issues > 0:
                        console.print(f"\n[yellow]Found {total_issues} issues[/yellow]\n")
                        
                        # Create a table to display issues by step
                        table = Table(title="Review Results")
                        table.add_column("Step", style="cyan")
                        table.add_column("Category", style="magenta")
                        table.add_column("Issues", style="yellow")
                        table.add_column("Duration (s)", style="blue")
                        
                        for step_id, step_result in step_results.items():
                            # Find the step instance with this ID
                            step_instance = next((s for s in filtered_instances if s.id == step_id), None)
                            category_name = step_instance.category.name if step_instance else "Unknown"
                            issues_count = len(step_result.get("issues", []))
                            duration = step_result.get("duration", 0)
                            table.add_row(
                                step_id, 
                                category_name, 
                                str(issues_count),
                                f"{duration:.2f}"
                            )
                        
                        console.print(table)
                        
                        # Display detailed issues
                        console.print("\n[bold]Detailed Issues:[/bold]")
                        for step_id, step_result in step_results.items():
                            if step_result.get("issues"):
                                console.print(f"\n[bold cyan]{step_id}[/bold cyan]:")
                                for issue in step_result.get("issues", []):
                                    console.print(f"  • {issue}")
                    else:
                        console.print("\n[green]No issues found![/green]")
                else:
                    console.print(f"\n[red]Review failed:[/red] {result.get('message', 'Unknown error')}")
            except Exception as e:
                console.print(f"\n[red]✗ An unexpected error occurred:[/red] {str(e)}")
                if debug:
                    import traceback
                    console.print("\n[bold]Debug: Traceback[/bold]")
                    console.print(traceback.format_exc())
        else:
            console.print("\n[yellow]No review steps selected after filtering.[/yellow]")
            console.print("Try adjusting the focus area or severity level.")
    
    console.print(f"[green]Report format:[/green] {output_format.value}")
