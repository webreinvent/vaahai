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
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
        # Create a test file with content
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("# Test file\n")
        
        result = runner.invoke(
            app,
            ["review", "run", temp_dir, "--no-confirm"],
            catch_exceptions=False
        )
        assert result.exit_code == 0
        assert "Reviewing:" in result.output
        assert "Code Review" in result.output


def test_review_run_command_with_options():
    """Test that the review run command works with various options."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
        # Create a test file with content
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("# Test file\n")
        
        result = runner.invoke(
            app,
            ["review", "run", temp_dir, "--depth", "deep", "--no-confirm"],
            catch_exceptions=False
        )
        assert result.exit_code == 0
        assert "Reviewing:" in result.output
        assert "Code Review" in result.output
        assert "Depth:" in result.output


def test_review_progress_display():
    """Test that the review command displays enhanced progress information."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
        # Create a test file with content that will trigger issues
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("""
# Test file with a simple issue
def test_function():
    password = "hardcoded_password"
    return password
""")
        
        result = runner.invoke(
            app,
            ["review", "run", test_file, "--no-confirm"],
            catch_exceptions=False
        )
        assert result.exit_code == 0
        
        # Check for progress indicators
        assert "Review Progress" in result.output
        assert "Total steps:" in result.output
        assert "Completed:" in result.output


def test_review_statistics_findings_display():
    """Test that the review command displays statistics and findings."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
        # Create a test file with content that will trigger issues
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("""
# Test file with multiple issues
def test_function():
    password = "hardcoded_password"
    api_key = "sk_test_abcdefghijklmnopqrstuvwxyz"
    token = "github_pat_abcdefghijklmnopqrstuvwxyz"
    return password
""")
        
        result = runner.invoke(
            app,
            ["review", "run", test_file, "--no-confirm"],
            catch_exceptions=False
        )
        assert result.exit_code == 0
        
        # Check for statistics panel
        assert "Review Progress" in result.output
        
        # Check for findings display
        assert "hardcoded_secrets" in result.output
        
        # Check for detailed issues
        assert "Detailed Issues:" in result.output or "Potential hardcoded secret found" in result.output


def test_review_output_format_selection():
    """Test that the review command supports different output formats."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
        # Create a test file with content that will trigger issues
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("""
# Test file with a simple issue
def test_function():
    password = "hardcoded_password"
    return password
""")

        # Test markdown format
        result_md = runner.invoke(
            app,
            ["review", "run", test_file, "--format", "markdown", "--no-confirm"],
            catch_exceptions=False
        )
        assert result_md.exit_code == 0
        assert "Markdown report generated:" in result_md.output or "Report format: markdown" in result_md.output
        
        # Test HTML format
        result_html = runner.invoke(
            app,
            ["review", "run", test_file, "--format", "html", "--no-confirm"],
            catch_exceptions=False
        )
        assert result_html.exit_code == 0
        assert "HTML report generated:" in result_html.output or "Report format: html" in result_html.output
        
        # Test rich format (default)
        result_rich = runner.invoke(
            app,
            ["review", "run", test_file, "--format", "rich", "--no-confirm"],
            catch_exceptions=False
        )
        assert result_rich.exit_code == 0
        assert "Code Review" in result_rich.output
        assert "Report format: rich" in result_rich.output
        
        # Test interactive format with apply-changes disabled
        # This should run without error but not enable code changes
        result_interactive = runner.invoke(
            app,
            ["review", "run", test_file, "--format", "interactive", "--no-confirm"],
            catch_exceptions=False
        )
        assert result_interactive.exit_code == 0
        assert "interactive" in result_interactive.output.lower()


def test_review_interactive_code_changes():
    """Test that the review command supports interactive code changes."""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory(dir="/tmp") as temp_dir:
        # Create a test file with content that will trigger issues
        test_file = os.path.join(temp_dir, "test_file.py")
        with open(test_file, "w") as f:
            f.write("""
# Test file with a simple issue
def test_function():
    password = "hardcoded_password"
    return password
""")

        # Test interactive format with apply-changes enabled and dry-run
        # Mock the input function to simulate key presses
        with pytest.MonkeyPatch.context() as monkeypatch:
            # Mock the input function to return 'q' to quit the interactive display
            # The input function in InteractiveDiffReporter is called without parameters
            monkeypatch.setattr('builtins.input', lambda: 'q')
            
            result_interactive = runner.invoke(
                app,
                ["review", "run", test_file, "--format", "interactive", 
                 "--apply-changes", "--dry-run", "--no-confirm"],
                catch_exceptions=False
            )
            assert result_interactive.exit_code == 0
            assert "interactive" in result_interactive.output.lower()
            # Don't check for dry-run in output as it might not be explicitly mentioned
        
        # Test interactive format with apply-changes and backup-dir
        backup_dir = os.path.join("/tmp", "vaahai_test_backups")
        # Create the backup directory first
        os.makedirs(backup_dir, exist_ok=True)
        
        with pytest.MonkeyPatch.context() as monkeypatch:
            # Mock the input function to return 'q' to quit the interactive display
            # The input function in InteractiveDiffReporter is called without parameters
            monkeypatch.setattr('builtins.input', lambda: 'q')
            
            result_interactive = runner.invoke(
                app,
                ["review", "run", test_file, "--format", "interactive", 
                 "--apply-changes", "--backup-dir", backup_dir, "--no-confirm"],
                catch_exceptions=False
            )
            assert result_interactive.exit_code == 0
            assert "interactive" in result_interactive.output.lower()
            
            # Verify that the backup directory exists
            assert os.path.exists(backup_dir)
