#!/usr/bin/env python3
"""
Example script demonstrating the HTML report generator functionality.

This script creates a mock review result and generates an HTML report.
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaahai.reporting.html_reporter import generate_html_report


def create_mock_review_result():
    """Create a mock review result for demonstration purposes."""
    return {
        "status": "success",
        "message": "Code review completed successfully",
        "total_issues": 5,
        "results": [
            {
                "step_id": "line_length",
                "step_name": "Line Length Check",
                "step_category": "code_style",
                "step_severity": "low",
                "file_path": "example/test_file.py",
                "issues": [
                    {
                        "line": 10,
                        "message": "Line exceeds maximum length (88 characters)",
                        "code": "def very_long_function_name_that_exceeds_line_length_limit(parameter1, parameter2, parameter3, parameter4):"
                    },
                    {
                        "line": 15,
                        "message": "Line exceeds maximum length (88 characters)",
                        "code": "    return 'This is a very long string that exceeds the maximum line length limit of 88 characters set by the style guide'"
                    }
                ]
            },
            {
                "step_id": "unused_imports",
                "step_name": "Unused Imports Check",
                "step_category": "code_quality",
                "step_severity": "medium",
                "file_path": "example/test_file.py",
                "issues": [
                    {
                        "line": 3,
                        "message": "Unused import: 'datetime'",
                        "code": "import os\nimport sys\nimport datetime  # Unused import"
                    }
                ]
            },
            {
                "step_id": "security_check",
                "step_name": "Security Vulnerability Check",
                "step_category": "security",
                "step_severity": "critical",
                "file_path": "example/test_file.py",
                "issues": [
                    {
                        "line": 42,
                        "message": "Hardcoded credentials detected",
                        "code": "password = 'admin123'  # Security risk: hardcoded password"
                    },
                    {
                        "line": 45,
                        "message": "Insecure cryptographic algorithm (MD5)",
                        "code": "import hashlib\n\ndef hash_password(password):\n    return hashlib.md5(password.encode()).hexdigest()  # Insecure: MD5 is vulnerable"
                    }
                ]
            }
        ],
        "key_findings": [
            {
                "type": "severity",
                "severity": "critical",
                "count": 2,
                "message": "Security vulnerabilities detected including hardcoded credentials and insecure cryptographic algorithms"
            },
            {
                "type": "severity",
                "severity": "medium",
                "count": 1,
                "message": "Code quality issues found including unused imports"
            },
            {
                "type": "severity",
                "severity": "low",
                "count": 2,
                "message": "Code style issues detected including lines exceeding maximum length"
            }
        ],
        "recommendations": [
            "Remove hardcoded credentials and use environment variables or a secure vault",
            "Replace MD5 with a more secure hashing algorithm like bcrypt or Argon2",
            "Remove unused imports to improve code quality",
            "Refactor long lines to improve readability"
        ],
        "statistics": {
            "total_files": 1,
            "files_with_issues": 1,
            "files_with_issues_percentage": 100.0,
            "total_issues": 5,
            "issues_per_file": 5.0,
            "issues_by_severity": {
                "critical": 2,
                "high": 0,
                "medium": 1,
                "low": 2,
                "info": 0
            },
            "issues_by_category": {
                "security": 2,
                "code_quality": 1,
                "code_style": 2
            },
            "most_common_issues": [
                ["Line exceeds maximum length", 2],
                ["Security vulnerabilities", 2],
                ["Unused imports", 1]
            ]
        },
        "progress": {
            "total_steps": 3,
            "completed_steps": 3,
            "failed_steps": 0,
            "skipped_steps": 0,
            "total_duration": 0.45
        }
    }


def main():
    """Generate an HTML report from mock review results and save it to a file."""
    # Create mock review result
    result = create_mock_review_result()
    
    # Generate HTML report
    html_report = generate_html_report(result)
    
    # Create a report file with timestamp
    report_path = f"vaahai_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_path, "w") as f:
        f.write(html_report)
    
    print(f"HTML report generated: {report_path}")
    print(f"Report size: {len(html_report)} characters")
    
    # Print a preview
    preview_length = min(200, len(html_report))
    print("\nPreview of the HTML report:")
    print("-" * 50)
    print(html_report[:preview_length] + "..." if len(html_report) > preview_length else html_report)
    print("-" * 50)
    
    return report_path


if __name__ == "__main__":
    main()
