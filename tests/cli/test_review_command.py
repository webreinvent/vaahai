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
