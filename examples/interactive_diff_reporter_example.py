#!/usr/bin/env python
"""
Example script demonstrating the use of the interactive diff reporter.

This script creates mock review results and displays them using the
InteractiveDiffReporter class, showing how to use the interactive
code diff display feature.
"""

import os
import sys
from rich.console import Console

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vaahai.reporting.interactive_diff_reporter import InteractiveDiffReporter, generate_interactive_diff_report


def create_mock_review_results():
    """Create mock review results for demonstration."""
    return {
        "status": "success",
        "progress": {
            "total_steps": 3,
            "completed_steps": 3,
            "failed_steps": 0,
            "skipped_steps": 0,
            "total_duration": 2.5
        },
        "statistics": {
            "total_files": 5,
            "files_with_issues": 3,
            "files_with_issues_percentage": 60.0,
            "total_issues": 4,
            "issues_per_file": 0.8,
            "issues_by_severity": {
                "critical": 1,
                "high": 0,
                "medium": 2,
                "low": 1,
                "info": 0
            }
        },
        "key_findings": [
            "Found 1 critical security issue: hardcoded credentials",
            "2 files have code style issues that should be addressed"
        ],
        "recommendations": [
            "Fix the critical security issue by using environment variables for credentials",
            "Address code style issues to improve maintainability"
        ],
        "results": {
            "style_check": {
                "step_id": "style_check",
                "status": "completed",
                "issues": [
                    {
                        "severity": "medium",
                        "message": "Line too long (90 characters)",
                        "file_path": "example_code/long_lines.py",
                        "line_number": 42,
                        "code_snippet": "def very_long_function_name_that_exceeds_line_length_limit(param1, param2, param3, param4, param5):",
                        "suggested_code": "def very_long_function_name_that_exceeds_line_length_limit(\n    param1, param2, param3, param4, param5):"
                    },
                    {
                        "severity": "low",
                        "message": "Missing docstring",
                        "file_path": "example_code/missing_docs.py",
                        "line_number": 15,
                        "code_snippet": "def helper_function(x, y):\n    return x + y",
                        "suggested_code": "def helper_function(x, y):\n    \"\"\"Add two numbers and return the result.\"\"\"\n    return x + y"
                    }
                ]
            },
            "security_check": {
                "step_id": "security_check",
                "status": "completed",
                "issues": [
                    {
                        "severity": "critical",
                        "message": "Hardcoded credentials",
                        "file_path": "example_code/config.py",
                        "line_number": 10,
                        "code_snippet": "PASSWORD = \"supersecret123\"",
                        "suggested_code": "PASSWORD = os.environ.get(\"APP_PASSWORD\")"
                    }
                ]
            },
            "performance_check": {
                "step_id": "performance_check",
                "status": "completed",
                "issues": [
                    {
                        "severity": "medium",
                        "message": "Inefficient list comprehension",
                        "file_path": "example_code/performance.py",
                        "line_number": 25,
                        "code_snippet": "result = [calculate_expensive_operation(x) for x in range(1000)]",
                        "suggested_code": "result = []\nfor x in range(1000):\n    if x % 10 == 0:  # Only process every 10th item\n        result.append(calculate_expensive_operation(x))"
                    }
                ]
            }
        }
    }


def main():
    """Run the example script."""
    console = Console()
    
    console.print("[bold blue]VaahAI Interactive Diff Reporter Example[/bold blue]")
    console.print("This example demonstrates the interactive code diff display feature.")
    console.print("In a real terminal, you would navigate through issues using arrow keys and press 'q' to quit.\n")
    
    # Create mock review results
    mock_results = create_mock_review_results()
    
    # Display a static preview of the interactive report
    console.print("[bold green]Interactive Code Diff Display Preview:[/bold green]")
    
    # Create a reporter instance
    reporter = InteractiveDiffReporter(mock_results, console)
    
    # Generate and display the layout without interactive navigation
    layout = reporter._generate_layout()
    console.print(layout)
    
    # Show navigation instructions
    console.print("\n[italic]In an actual terminal session, you would be able to navigate through issues and files.[/italic]")
    console.print("[italic]This is just a static preview of the interactive display.[/italic]")
    
    console.print("\n[bold green]Example completed![/bold green]")


if __name__ == "__main__":
    main()
