"""
Tests for VaahAI review command.

This module contains tests to verify that the review command and its subcommands
function correctly.
"""

import tempfile
import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app

runner = CliRunner()


def test_review_run_command_with_directory():
    """Test that the review run command works with a directory path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(app, ["review", "run", temp_dir])
        assert result.exit_code == 0
        assert "Code Review" in result.stdout
        assert temp_dir in result.stdout
        assert "Depth: standard" in result.stdout
        # Check for language/framework detection output
        assert "Language:" in result.stdout
        assert "Framework:" in result.stdout


def test_review_run_command_with_options():
    """Test that the review run command works with various options."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(
            app,
            ["review", "run", temp_dir, "--depth", "thorough", "--focus", "security"],
        )
        assert result.exit_code == 0
        assert "Code Review" in result.stdout
        assert "Depth: thorough" in result.stdout
        assert "Focus: security" in result.stdout
        # Check for language/framework detection output
        assert "Language:" in result.stdout
        assert "Framework:" in result.stdout


def test_review_progress_display():
    """Test that the review command displays enhanced progress information."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file to review
        test_file = Path(temp_dir) / "test_file.py"
        with open(test_file, "w") as f:
            f.write("def test_function():\n    x = 1\n    return x\n")
        
        result = runner.invoke(app, ["review", "run", str(test_file)])
        
        assert result.exit_code == 0
        
        # Verify progress display components
        assert "Running review steps" in result.stdout
        
        # Check for emoji indicators in the output
        assert "✅" in result.stdout  # Completed steps
        
        # Check for statistics panel
        assert "Review Statistics" in result.stdout
        assert "Total steps:" in result.stdout
        assert "Completed:" in result.stdout
        assert "Total duration:" in result.stdout


def test_review_statistics_findings_display():
    """Test that the review command displays statistics and findings."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file with content that will trigger issues
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("""
# This file has several issues for testing
import os
import sys
import subprocess

# SQL Injection vulnerability
def execute_query(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

# Inefficient loop
def process_items(items):
    result = []
    for i in range(len(items)):
        result.append(items[i] * 2)
    return result

# Hardcoded credentials
PASSWORD = "supersecret123"
API_KEY = "abcd1234"

# Command injection
def run_command(user_input):
    os.system("echo " + user_input)
    return subprocess.check_output("ls " + user_input, shell=True)
""")

        # Run the review command
        runner = CliRunner()
        result = runner.invoke(
            app,
            ["review", "run", test_file, "--no-confirm"],
            catch_exceptions=False
        )
        
        # Check that the command executed successfully
        assert result.exit_code == 0
        
        # Verify that statistics are displayed
        assert "Review Statistics" in result.output
        assert "Files reviewed:" in result.output
        assert "Total issues:" in result.output
        assert "Issues by Severity:" in result.output
        assert "Issues by Category:" in result.output
        
        # Verify that key findings are displayed
        assert "Key Findings" in result.output
        
        # Verify that recommendations are displayed
        assert "Recommendations" in result.output
        
        # Check for emoji indicators in statistics and findings
        severity_emojis = ["🔴", "🟠", "🟡", "🟢", "🔵"]
        category_emojis = ["🔒", "⚡", "✨", "🧩", "🔧"]
        
        # At least one severity emoji should be present
        assert any(emoji in result.output for emoji in severity_emojis)
        
        # At least one category emoji should be present
        assert any(emoji in result.output for emoji in category_emojis)
