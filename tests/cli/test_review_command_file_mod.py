"""
Tests for VaahAI review command file modification options.

This module contains tests to verify that the review command's file modification
options function correctly.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app
from vaahai.utils.code_change_manager import CodeChangeManager
from vaahai.reporting.interactive_diff_reporter import InteractiveDiffReporter


@pytest.fixture
def mock_code_file():
    """Create a temporary Python file with some code issues for testing."""
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        temp_file.write(b"""def very_long_function_name_that_exceeds_line_length_limit(param1, param2, param3, param4, param5):
    # This function has a line that is too long
    return param1 + param2 + param3 + param4 + param5

def missing_docstring_function():
    return True
""")
        temp_path = temp_file.name
    
    yield temp_path
    
    # Clean up
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@patch("vaahai.cli.commands.review.command.CodeChangeManager")
def test_review_run_with_apply_changes_option(mock_code_change_manager, mock_code_file):
    """Test that the review run command works with the apply-changes option."""
    # Mock the CodeChangeManager instance
    mock_manager = MagicMock()
    mock_code_change_manager.return_value = mock_manager
    
    # Run the command with apply-changes option
    result = runner.invoke(
        app,
        ["review", "run", mock_code_file, "--apply-changes"],
    )
    
    # Verify the command executed successfully
    assert result.exit_code == 0
    
    # Verify CodeChangeManager was instantiated
    mock_code_change_manager.assert_called_once()
    
    # Verify the output mentions applying changes
    assert "Code changes can be applied interactively" in result.stdout


@patch("vaahai.cli.commands.review.command.CodeChangeManager")
def test_review_run_with_dry_run_option(mock_code_change_manager, mock_code_file):
    """Test that the review run command works with the dry-run option."""
    # Mock the CodeChangeManager instance
    mock_manager = MagicMock()
    mock_code_change_manager.return_value = mock_manager
    
    # Run the command with apply-changes and dry-run options
    result = runner.invoke(
        app,
        ["review", "run", mock_code_file, "--apply-changes", "--dry-run"],
    )
    
    # Verify the command executed successfully
    assert result.exit_code == 0
    
    # Verify CodeChangeManager was instantiated with dry_run=True
    mock_code_change_manager.assert_called_once_with(
        dry_run=True,
        backup_dir=mock_manager.backup_dir,
        require_confirmation=True
    )
    
    # Verify the output mentions dry run mode
    assert "DRY RUN MODE" in result.stdout


@patch("vaahai.cli.commands.review.command.CodeChangeManager")
def test_review_run_with_backup_dir_option(mock_code_change_manager, mock_code_file):
    """Test that the review run command works with the backup-dir option."""
    # Mock the CodeChangeManager instance
    mock_manager = MagicMock()
    mock_code_change_manager.return_value = mock_manager
    
    # Create a temporary backup directory
    with tempfile.TemporaryDirectory() as backup_dir:
        # Run the command with apply-changes and backup-dir options
        result = runner.invoke(
            app,
            ["review", "run", mock_code_file, "--apply-changes", "--backup-dir", backup_dir],
        )
        
        # Verify the command executed successfully
        assert result.exit_code == 0
        
        # Verify CodeChangeManager was instantiated with the custom backup directory
        mock_code_change_manager.assert_called_once_with(
            dry_run=False,
            backup_dir=backup_dir,
            require_confirmation=True
        )


@patch("vaahai.cli.commands.review.command.CodeChangeManager")
def test_review_run_with_no_confirm_option(mock_code_change_manager, mock_code_file):
    """Test that the review run command works with the no-confirm option."""
    # Mock the CodeChangeManager instance
    mock_manager = MagicMock()
    mock_code_change_manager.return_value = mock_manager
    
    # Run the command with apply-changes and no-confirm options
    result = runner.invoke(
        app,
        ["review", "run", mock_code_file, "--apply-changes", "--no-confirm"],
    )
    
    # Verify the command executed successfully
    assert result.exit_code == 0
    
    # Verify CodeChangeManager was instantiated with require_confirmation=False
    mock_code_change_manager.assert_called_once_with(
        dry_run=False,
        backup_dir=mock_manager.backup_dir,
        require_confirmation=False
    )
    
    # Verify the output mentions no confirmation mode
    assert "Confirmation prompts are disabled" in result.stdout


@patch("vaahai.cli.commands.review.command.generate_interactive_diff_report")
@patch("vaahai.cli.commands.review.command.CodeChangeManager")
def test_review_run_passes_manager_to_reporter(mock_code_change_manager, mock_generate_report, mock_code_file):
    """Test that the CodeChangeManager is passed to the InteractiveDiffReporter."""
    # Mock the CodeChangeManager instance
    mock_manager = MagicMock()
    mock_code_change_manager.return_value = mock_manager
    
    # Run the command with apply-changes option
    result = runner.invoke(
        app,
        ["review", "run", mock_code_file, "--apply-changes", "--output", "interactive"],
    )
    
    # Verify the command executed successfully
    assert result.exit_code == 0
    
    # Verify generate_interactive_diff_report was called with the manager
    mock_generate_report.assert_called_once()
    args, kwargs = mock_generate_report.call_args
    assert kwargs.get("code_change_manager") == mock_manager


@patch("vaahai.cli.commands.review.command.CodeChangeManager")
def test_review_run_without_apply_changes_option(mock_code_change_manager, mock_code_file):
    """Test that the review run command doesn't use CodeChangeManager without apply-changes option."""
    # Run the command without apply-changes option
    result = runner.invoke(
        app,
        ["review", "run", mock_code_file],
    )
    
    # Verify the command executed successfully
    assert result.exit_code == 0
    
    # Verify CodeChangeManager was not instantiated
    mock_code_change_manager.assert_not_called()
