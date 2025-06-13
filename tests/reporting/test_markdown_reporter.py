"""Tests for the markdown reporter implementation."""

import os
import tempfile
from pathlib import Path
import re
from datetime import datetime

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app
from vaahai.reporting.markdown_reporter import MarkdownReporter, generate_markdown_report
from vaahai.reporting.formats import OutputFormat


def test_markdown_reporter_initialization():
    """Test that the MarkdownReporter can be initialized."""
    reporter = MarkdownReporter({})
    assert reporter is not None


def test_generate_markdown_report():
    """Test that generate_markdown_report returns a markdown string."""
    result = {
        "status": "success",
        "message": "Review completed successfully",
        "results": {},
        "total_issues": 0,
        "output_format": OutputFormat.MARKDOWN
    }
    report = generate_markdown_report(result)
    assert isinstance(report, str)
    assert "# VaahAI Code Review Report" in report
    assert "## Summary" in report


def test_markdown_report_with_issues():
    """Test that the markdown report includes issues when present."""
    result = {
        "status": "success",
        "message": "Review completed successfully",
        "results": {
            "test_step": {
                "step_id": "test_step",
                "status": "success",
                "issues": [
                    "This is a test issue"
                ],
                "duration": 0.5
            }
        },
        "total_issues": 1,
        "statistics": {
            "total_issues": 1,
            "issues_by_severity": {"medium": 1},
            "issues_by_category": {"style": 1},
            "most_common_issues": [["This is a test issue", 1]]
        },
        "key_findings": [
            {"type": "severity", "severity": "medium", "count": 1, "message": "Test finding"}
        ],
        "recommendations": [
            {"type": "style", "message": "Test recommendation"}
        ],
        "output_format": OutputFormat.MARKDOWN
    }
    report = generate_markdown_report(result)
    assert "## Detailed Issues" in report
    assert "### Issues by Step" in report
    assert "#### test_step" in report
    assert "This is a test issue" in report
    assert "## Key Findings" in report
    assert "Test finding" in report
    assert "## Actionable Recommendations" in report
    assert "Test recommendation" in report


def test_cli_markdown_format_generates_file():
    """Test that the CLI command generates a markdown file when markdown format is selected."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file with some content
        test_file = Path(temp_dir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write("def test_function():\n    x = 1\n    y = 2\n    return x + y\n")
        
        # Run the review command with markdown format
        result = runner.invoke(app, ["review", "run", str(test_file), "--format", "markdown", "--depth", "quick"], input="\n")
        
        # Check that the command was successful
        assert result.exit_code == 0, result.stderr
        
        # Check that the output mentions a markdown report was generated
        assert "Markdown report generated:" in result.stdout
        
        # Extract the report path from the output
        match = re.search(r"Markdown report generated: ([\w\./_-]+\.md)", result.stdout)
        assert match is not None
        report_path = match.group(1)
        
        # Check that the file exists
        assert os.path.exists(report_path)
        
        # Check the content of the file
        with open(report_path, "r") as f:
            content = f.read()
            assert "# VaahAI Code Review Report" in content
            assert "## Summary" in content
            
        # Clean up the generated file
        os.remove(report_path)


# Define the CLI runner at module level
runner = CliRunner(mix_stderr=False)
