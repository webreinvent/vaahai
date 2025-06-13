"""
Tests for VaahAI review command.

This module contains tests to verify that the review command and its subcommands
function correctly.
"""

import tempfile
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
