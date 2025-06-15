"""
Tests for the VaahAI CLI warning system.

This module contains tests for the warning system that displays
configuration warnings across all CLI commands.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app
from vaahai.cli.utils.warning_system import (
    WarningSystem,
    WarningMessage,
    WarningCategory,
    WarningLevel,
    check_and_display_warnings,
)
from vaahai.utils.config_validator import ConfigValidator, ValidationLevel, ValidationResult


@pytest.fixture
def cli_runner():
    """Create a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def mock_config_validator():
    """Mock the ConfigValidator class for testing."""
    with patch("vaahai.cli.utils.warning_system.ConfigValidator") as mock:
        # Set up the mock to return a specific validation result
        validator_instance = MagicMock()
        
        # Default to not configured
        mock.is_configured.return_value = False
        
        # Default validation results
        validator_instance.validate.return_value = (
            False,  # is_valid
            [
                ValidationResult(
                    key="config.file",
                    valid=False,
                    level=ValidationLevel.ERROR,
                    message="Configuration file does not exist",
                ),
                ValidationResult(
                    key="llm.openai.api_key",
                    valid=False,
                    level=ValidationLevel.ERROR,
                    message="API key for OpenAI is not configured",
                ),
            ],
        )
        
        mock.return_value = validator_instance
        yield mock


def test_warning_message_str():
    """Test the string representation of a warning message."""
    warning = WarningMessage(
        level=WarningLevel.WARNING,
        category=WarningCategory.CONFIGURATION,
        message="Test warning message",
    )
    
    assert str(warning) == "⚠️ Test warning message"


def test_warning_message_rich_panel():
    """Test the Rich panel representation of a warning message."""
    warning = WarningMessage(
        level=WarningLevel.ERROR,
        category=WarningCategory.CONFIGURATION,
        message="Test error message",
        details="This is a test error message",
        fix_command="vaahai config init",
        docs_url="https://docs.vaahai.io/configuration",
    )
    
    panel = warning.get_rich_panel()
    assert panel.title == "Error [Configuration]"
    assert panel.border_style == "red"
    
    # Check that the panel content contains the expected elements
    content = panel.renderable
    assert "Test error message" in str(content)
    assert "This is a test error message" in str(content)
    assert "vaahai config init" in str(content)
    assert "https://docs.vaahai.io/configuration" in str(content)


def test_warning_system_add_warning():
    """Test adding warnings to the warning system."""
    system = WarningSystem()
    
    warning1 = WarningMessage(
        level=WarningLevel.ERROR,
        category=WarningCategory.CONFIGURATION,
        message="Test error message",
    )
    
    warning2 = WarningMessage(
        level=WarningLevel.WARNING,
        category=WarningCategory.DEPENDENCY,
        message="Test warning message",
    )
    
    system.add_warning(warning1)
    system.add_warning(warning2)
    
    assert len(system.warnings) == 2
    assert system.warnings[0] == warning1
    assert system.warnings[1] == warning2


def test_warning_system_add_config_warnings(mock_config_validator):
    """Test adding configuration warnings based on ConfigValidator results."""
    system = WarningSystem()
    system.add_config_warnings()
    
    # Should have two warnings from the mock validator
    assert len(system.warnings) == 2
    
    # Check the first warning
    assert system.warnings[0].level == WarningLevel.ERROR
    assert system.warnings[0].category == WarningCategory.CONFIGURATION
    assert "configuration file" in system.warnings[0].message.lower()
    assert system.warnings[0].fix_command == "vaahai config init"
    
    # Check the second warning
    assert system.warnings[1].level == WarningLevel.ERROR
    assert system.warnings[1].category == WarningCategory.CONFIGURATION
    assert "api key" in system.warnings[1].message.lower()
    assert "openai" in system.warnings[1].message.lower()
    assert "vaahai config set" in system.warnings[1].fix_command


def test_warning_system_display_warnings():
    """Test displaying warnings from the warning system."""
    system = WarningSystem()
    
    # Add some warnings
    system.add_warning(
        WarningMessage(
            level=WarningLevel.ERROR,
            category=WarningCategory.CONFIGURATION,
            message="Test error message",
        )
    )
    
    system.add_warning(
        WarningMessage(
            level=WarningLevel.WARNING,
            category=WarningCategory.DEPENDENCY,
            message="Test warning message",
        )
    )
    
    system.add_warning(
        WarningMessage(
            level=WarningLevel.INFO,
            category=WarningCategory.GENERAL,
            message="Test info message",
        )
    )
    
    # Test with mock console to capture output
    with patch("vaahai.cli.utils.warning_system.console") as mock_console:
        # Display all warnings
        result = system.display_warnings()
        
        # Should return True because warnings were displayed
        assert result is True
        
        # Console should have been called multiple times
        assert mock_console.print.call_count >= 3  # Header + at least one warning
        
        # Reset mock
        mock_console.reset_mock()
        
        # Display only errors
        result = system.display_warnings(min_level=WarningLevel.ERROR)
        
        # Should return True because warnings were displayed
        assert result is True
        
        # Console should have been called once
        assert mock_console.print.call_count >= 1
        
        # Reset mock
        mock_console.reset_mock()
        
        # Display only configuration warnings
        result = system.display_warnings(categories=[WarningCategory.CONFIGURATION])
        
        # Should return True because warnings were displayed
        assert result is True
        
        # Console should have been called at least once
        assert mock_console.print.call_count >= 1


def test_warning_system_quiet_mode():
    """Test that warnings are suppressed in quiet mode."""
    system = WarningSystem(quiet=True)
    
    # Add a warning
    system.add_warning(
        WarningMessage(
            level=WarningLevel.ERROR,
            category=WarningCategory.CONFIGURATION,
            message="Test error message",
        )
    )
    
    # Test with mock console to capture output
    with patch("vaahai.cli.utils.warning_system.console") as mock_console:
        # Display warnings
        result = system.display_warnings()
        
        # Should return False because no warnings were displayed
        assert result is False
        
        # Console should not have been called
        mock_console.print.assert_not_called()


def test_check_and_display_warnings(mock_config_validator):
    """Test the check_and_display_warnings convenience function."""
    # Test with mock console to capture output
    with patch("vaahai.cli.utils.warning_system.console") as mock_console:
        # Check and display warnings
        result = check_and_display_warnings(
            command_name="test",
            categories=[WarningCategory.CONFIGURATION],
            min_level=WarningLevel.WARNING,
        )
        
        # Should return True because warnings were displayed
        assert result is True
        
        # Console should have been called multiple times
        assert mock_console.print.call_count >= 3  # Header + 2 warnings
        
        # Reset mock
        mock_console.reset_mock()
        
        # Check and display warnings in quiet mode
        result = check_and_display_warnings(
            command_name="test",
            categories=[WarningCategory.CONFIGURATION],
            min_level=WarningLevel.WARNING,
            quiet=True,
        )
        
        # Should return False because no warnings were displayed
        assert result is False
        
        # Console should not have been called
        mock_console.print.assert_not_called()


def test_cli_command_with_warnings():
    """Test that CLI commands display warnings when appropriate."""
    # We'll test the integration at a higher level
    # by directly testing the warning system functionality
    system = WarningSystem()
    system.add_warning(
        WarningMessage(
            level=WarningLevel.ERROR,
            category=WarningCategory.CONFIGURATION,
            message="Test error message",
        )
    )
    
    with patch("vaahai.cli.utils.warning_system.console") as mock_console:
        result = system.display_warnings(command_context="version")
        assert result is True
        assert mock_console.print.call_count >= 2  # Header + warning


def test_cli_config_command_no_warnings():
    """Test that config commands don't display warnings."""
    # For config commands, we don't show warnings
    # This is handled in the main.py callback function
    # We'll test this by directly checking if the command starts with 'config'
    
    # Create a warning system
    system = WarningSystem()
    
    # Test with a config command
    with patch("vaahai.cli.utils.warning_system.console") as mock_console:
        # This should not display warnings for config commands
        result = check_and_display_warnings(
            command_name="config",
            categories=[WarningCategory.CONFIGURATION],
        )
        
        # Should return False because no warnings should be displayed for config commands
        assert result is False
        
        # Console should not have been called
        mock_console.print.assert_not_called()


def test_cli_command_no_warnings_when_configured():
    """Test that CLI commands don't display warnings when VaahAI is configured."""
    # When VaahAI is configured, the warning system should not show warnings
    # We'll test this by mocking the ConfigValidator
    with patch("vaahai.cli.utils.warning_system.ConfigValidator") as mock_validator:
        # Set up the mock to return configured
        validator_instance = MagicMock()
        mock_validator.is_configured.return_value = True
        validator_instance.validate.return_value = (True, [])
        mock_validator.return_value = validator_instance
        
        # Create a warning system
        system = WarningSystem()
        
        # Add config warnings (should not add any since we're configured)
        system.add_config_warnings()
        
        # Should not have any warnings
        assert len(system.warnings) == 0


def test_cli_command_with_quiet_flag():
    """Test that warnings are suppressed with the --quiet flag."""
    # When quiet flag is set, the warning system should not show warnings
    system = WarningSystem(quiet=True)
    
    # Add a warning
    system.add_warning(
        WarningMessage(
            level=WarningLevel.ERROR,
            category=WarningCategory.CONFIGURATION,
            message="Test error message",
        )
    )
    
    # Test with mock console to capture output
    with patch("vaahai.cli.utils.warning_system.console") as mock_console:
        # Display warnings
        result = system.display_warnings()
        
        # Should return False because no warnings were displayed
        assert result is False
        
        # Console should not have been called
        mock_console.print.assert_not_called()
