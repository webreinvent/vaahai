#!/usr/bin/env python
"""
Example script demonstrating the markdown report generator functionality.

This script shows how to use the markdown reporter to generate a markdown report
from review results.
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaahai.reporting.markdown_reporter import generate_markdown_report
from vaahai.reporting.formats import OutputFormat


def create_sample_review_result():
    """Create a sample review result for demonstration."""
    return {
        "status": "success",
        "message": "Review completed successfully",
        "results": {
            "LineLength": {
                "step_id": "LineLength",
                "status": "success",
                "issues": [
                    "Line 10: Line exceeds 80 characters (95 characters)",
                    "Line 25: Line exceeds 80 characters (88 characters)"
                ],
                "duration": 0.15,
                "file_path": "example_code.py"
            },
            "IndentationConsistency": {
                "step_id": "IndentationConsistency",
                "status": "success",
                "issues": [
                    "Line 15: Inconsistent indentation (expected 4 spaces, found 2 spaces)"
                ],
                "duration": 0.08,
                "file_path": "example_code.py"
            },
            "SQLInjection": {
                "step_id": "SQLInjection",
                "status": "success",
                "issues": [
                    "Line 42: Possible SQL injection vulnerability in query"
                ],
                "duration": 0.25,
                "file_path": "example_code.py"
            }
        },
        "total_issues": 4,
        "statistics": {
            "total_issues": 4,
            "total_files": 1,
            "files_with_issues": 1,
            "files_with_issues_percentage": 100.0,
            "issues_per_file": 4.0,
            "issues_by_severity": {
                "critical": 1,
                "medium": 1,
                "low": 2
            },
            "issues_by_category": {
                "security": 1,
                "style": 3
            },
            "most_common_issues": [
                ["Line exceeds 80 characters", 2],
                ["Inconsistent indentation", 1],
                ["SQL injection vulnerability", 1]
            ]
        },
        "key_findings": [
            {
                "type": "severity",
                "severity": "critical",
                "count": 1,
                "message": "1 critical security issue found: SQL injection vulnerability"
            },
            {
                "type": "category",
                "category": "style",
                "count": 3,
                "message": "3 style issues found, including line length and indentation problems"
            }
        ],
        "recommendations": [
            {
                "type": "security",
                "message": "Fix SQL injection vulnerability by using parameterized queries"
            },
            {
                "type": "style",
                "message": "Configure your editor to enforce line length limits of 80 characters"
            },
            {
                "type": "style",
                "message": "Use consistent indentation (4 spaces) throughout your code"
            }
        ],
        "progress": {
            "total_steps": 3,
            "completed_steps": 3,
            "failed_steps": 0,
            "skipped_steps": 0,
            "total_duration": 0.48
        },
        "output_format": OutputFormat.MARKDOWN
    }


def main():
    """Run the example."""
    # Create a sample review result
    review_result = create_sample_review_result()
    
    # Generate a markdown report
    markdown_report = generate_markdown_report(review_result)
    
    # Save the report to a file
    report_path = f"example_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, "w") as f:
        f.write(markdown_report)
    
    print(f"Markdown report generated: {report_path}")
    
    # Print a preview of the report
    preview_length = min(500, len(markdown_report))
    print("\nReport Preview:")
    print("-" * 80)
    print(markdown_report[:preview_length] + ("..." if len(markdown_report) > preview_length else ""))
    print("-" * 80)


if __name__ == "__main__":
    main()
