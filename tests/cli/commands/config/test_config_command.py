"""
Tests for the config command.

This module contains tests for the config command implementation.
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app
from vaahai.config.manager import ConfigManager


@pytest.fixture
def mock_config_manager():
    """Mock ConfigManager for testing."""
    with patch("vaahai.cli.commands.config.command.ConfigManager") as mock:
        # Set up the mock to return a MagicMock instance
        mock_instance = MagicMock(spec=ConfigManager)
        mock.return_value = mock_instance
        
        # Configure common mock behaviors
        mock_instance.exists.return_value = True
        mock_instance.get_full_config.return_value = {
            "llm": {"provider": "openai"},
            "providers": {
                "openai": {"api_key": "test-key", "model": "gpt-4"},
                "claude": {"api_key": "", "model": ""},
                "junie": {"api_key": "", "model": ""},
                "ollama": {"api_key": "", "model": ""},
            },
            "docker": {"enabled": False, "image": "", "memory": "8g"},
            "output": {"format": "text", "color": True},
        }
        mock_instance.get_current_provider.return_value = "openai"
        mock_instance.validate.return_value = []
        mock_instance.save.return_value = True
        
        yield mock_instance


@pytest.fixture
def runner():
    """Typer CLI runner."""
    return CliRunner()


def test_config_show(runner, mock_config_manager):
    """Test the config show command."""
    # Configure mock behaviors specific to this test
    with patch("vaahai.cli.commands.config.command.list_providers") as mock_list_providers:
        mock_list_providers.return_value = ["openai", "claude", "junie", "ollama"]
        
        # Run the command
        result = runner.invoke(app, ["config", "show"])
        
        # Check the result
        assert result.exit_code == 0
        assert "VaahAI Configuration" in result.stdout
        assert "Active LLM Provider: openai" in result.stdout
        assert "Provider Settings" in result.stdout
        assert "Docker Settings" in result.stdout
        assert "Output Settings" in result.stdout
        
        # Verify mock calls
        mock_config_manager.exists.assert_called_once()
        mock_config_manager.get_full_config.assert_called_once()
        mock_config_manager.get_current_provider.assert_called_once()


def test_config_show_file_not_found(runner, mock_config_manager):
    """Test the config show command when the config file is not found."""
    # Configure mock behaviors specific to this test
    mock_config_manager.exists.return_value = False
    
    # Run the command
    result = runner.invoke(app, ["config", "show"])
    
    # Check the result
    assert result.exit_code == 1
    assert "Configuration file not found" in result.stdout
    assert "Run 'vaahai config init'" in result.stdout


def test_config_get(runner, mock_config_manager):
    """Test the config get command."""
    # Configure mock behaviors specific to this test
    mock_config_manager.get.return_value = "openai"
    
    # Run the command
    result = runner.invoke(app, ["config", "get", "llm.provider"])
    
    # Check the result
    assert result.exit_code == 0
    assert "llm.provider" in result.stdout
    assert "openai" in result.stdout
    
    # Verify mock calls
    mock_config_manager.get.assert_called_once_with("llm.provider")


def test_config_get_key_not_found(runner, mock_config_manager):
    """Test the config get command when the key is not found."""
    # Configure mock behaviors specific to this test
    mock_config_manager.get.return_value = None
    
    # Run the command
    result = runner.invoke(app, ["config", "get", "nonexistent.key"])
    
    # Check the result
    assert result.exit_code == 1
    assert "Configuration key not found" in result.stdout
    
    # Verify mock calls
    mock_config_manager.get.assert_called_once_with("nonexistent.key")


def test_config_set(runner, mock_config_manager):
    """Test the config set command."""
    # Run the command
    result = runner.invoke(app, ["config", "set", "llm.provider", "claude"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Configuration value set" in result.stdout
    
    # Verify mock calls
    mock_config_manager.set.assert_called_once_with("llm.provider", "claude")
    mock_config_manager.save.assert_called_once_with(user_level=True)


def test_config_set_project_level(runner, mock_config_manager):
    """Test the config set command at project level."""
    # Run the command
    result = runner.invoke(app, ["config", "set", "llm.provider", "claude", "--project"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Configuration value set" in result.stdout
    
    # Verify mock calls
    mock_config_manager.set.assert_called_once_with("llm.provider", "claude")
    mock_config_manager.save.assert_called_once_with(user_level=False)


def test_config_set_boolean(runner, mock_config_manager):
    """Test the config set command with boolean values."""
    # Run the command for true
    result_true = runner.invoke(app, ["config", "set", "docker.enabled", "true"])
    
    # Check the result
    assert result_true.exit_code == 0
    assert "Configuration value set" in result_true.stdout
    
    # Verify mock calls
    mock_config_manager.set.assert_called_with("docker.enabled", True)
    
    # Reset mock
    mock_config_manager.reset_mock()
    
    # Run the command for false
    result_false = runner.invoke(app, ["config", "set", "docker.enabled", "false"])
    
    # Check the result
    assert result_false.exit_code == 0
    assert "Configuration value set" in result_false.stdout
    
    # Verify mock calls
    mock_config_manager.set.assert_called_with("docker.enabled", False)


def test_config_set_numeric(runner, mock_config_manager):
    """Test the config set command with numeric values."""
    # Run the command for integer
    result_int = runner.invoke(app, ["config", "set", "docker.port", "8080"])
    
    # Check the result
    assert result_int.exit_code == 0
    assert "Configuration value set" in result_int.stdout
    
    # Verify mock calls
    mock_config_manager.set.assert_called_with("docker.port", 8080)
    
    # Reset mock
    mock_config_manager.reset_mock()
    
    # Run the command for float
    result_float = runner.invoke(app, ["config", "set", "llm.temperature", "0.7"])
    
    # Check the result
    assert result_float.exit_code == 0
    assert "Configuration value set" in result_float.stdout
    
    # Verify mock calls
    mock_config_manager.set.assert_called_with("llm.temperature", 0.7)


def test_config_reset_confirmed(runner, mock_config_manager):
    """Test the config reset command with confirmation."""
    # Run the command with --yes flag
    result = runner.invoke(app, ["config", "reset", "--yes"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Configuration reset to defaults" in result.stdout
    
    # Verify mock calls
    mock_config_manager.reset.assert_called_once()
    mock_config_manager.save.assert_called_once_with(user_level=True)


def test_config_reset_cancelled(runner, mock_config_manager):
    """Test the config reset command with cancellation."""
    # Mock the inquirer.confirm to return False
    with patch("vaahai.cli.commands.config.command.inquirer.confirm") as mock_confirm:
        mock_confirm_instance = MagicMock()
        mock_confirm_instance.execute.return_value = False
        mock_confirm.return_value = mock_confirm_instance
        
        # Run the command without --yes flag
        result = runner.invoke(app, ["config", "reset"])
        
        # Check the result
        assert result.exit_code == 0
        assert "Reset cancelled" in result.stdout
        
        # Verify mock calls
        mock_config_manager.reset.assert_not_called()
        mock_config_manager.save.assert_not_called()


@patch("vaahai.cli.commands.config.command.inquirer.select")
@patch("vaahai.cli.commands.config.command.inquirer.secret")
@patch("vaahai.cli.commands.config.command.inquirer.confirm")
@patch("vaahai.cli.commands.config.command.inquirer.text")
@patch("vaahai.cli.commands.config.command.list_providers")
@patch("vaahai.cli.commands.config.command.list_models")
def test_config_init(
    mock_list_models, 
    mock_list_providers, 
    mock_text, 
    mock_confirm, 
    mock_secret, 
    mock_select, 
    runner, 
    mock_config_manager
):
    """Test the config init command."""
    # Configure mock behaviors
    mock_list_providers.return_value = ["openai", "claude", "junie", "ollama"]
    mock_list_models.return_value = ["gpt-4", "gpt-3.5-turbo"]
    
    # Set up mock inquirer responses
    mock_select_instance = MagicMock()
    mock_select_instance.execute.side_effect = ["openai", "gpt-4"]
    mock_select.return_value = mock_select_instance
    
    mock_secret_instance = MagicMock()
    mock_secret_instance.execute.return_value = "new-api-key"
    mock_secret.return_value = mock_secret_instance
    
    mock_confirm_instance = MagicMock()
    mock_confirm_instance.execute.return_value = True
    mock_confirm.return_value = mock_confirm_instance
    
    mock_text_instance = MagicMock()
    mock_text_instance.execute.side_effect = ["custom-image", "16g"]
    mock_text.return_value = mock_text_instance
    
    # Run the command
    result = runner.invoke(app, ["config", "init"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Configuration saved successfully" in result.stdout
    
    # Verify mock calls
    mock_config_manager.set_provider.assert_called_once_with("openai")
    mock_config_manager.set_api_key.assert_called_once_with("new-api-key", "openai")
    mock_config_manager.set_model.assert_called_once_with("gpt-4", "openai")
    mock_config_manager.set.assert_any_call("docker.enabled", True)
    mock_config_manager.set.assert_any_call("docker.image", "custom-image")
    mock_config_manager.set.assert_any_call("docker.memory", "16g")
    mock_config_manager.save.assert_called_once_with(user_level=True)


@patch("vaahai.cli.commands.config.command.inquirer.select")
@patch("vaahai.cli.commands.config.command.inquirer.secret")
@patch("vaahai.cli.commands.config.command.inquirer.confirm")
@patch("vaahai.cli.commands.config.command.list_providers")
@patch("vaahai.cli.commands.config.command.list_models")
def test_config_init_api_key_validation_error(
    mock_list_models, 
    mock_list_providers, 
    mock_confirm, 
    mock_secret, 
    mock_select, 
    runner, 
    mock_config_manager
):
    """Test the config init command with API key validation error."""
    # Configure mock behaviors
    mock_list_providers.return_value = ["openai", "claude", "junie", "ollama"]
    mock_list_models.return_value = ["gpt-4", "gpt-3.5-turbo"]
    
    # Set up mock inquirer responses
    mock_select_instance = MagicMock()
    mock_select_instance.execute.side_effect = ["openai", "gpt-4"]
    mock_select.return_value = mock_select_instance
    
    mock_secret_instance = MagicMock()
    mock_secret_instance.execute.return_value = "invalid-key"
    mock_secret.return_value = mock_secret_instance
    
    mock_confirm_instance = MagicMock()
    mock_confirm_instance.execute.return_value = False
    mock_confirm.return_value = mock_confirm_instance
    
    # Make set_api_key raise ValueError
    mock_config_manager.set_api_key.side_effect = ValueError("Invalid API key")
    
    # Run the command
    result = runner.invoke(app, ["config", "init"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Could not validate API key" in result.stdout
    assert "The key will be saved but might not work correctly" in result.stdout
    
    # Verify mock calls
    mock_config_manager.set_provider.assert_called_once_with("openai")
    mock_config_manager.set_api_key.assert_called_once_with("invalid-key", "openai")
    mock_config_manager.set.assert_any_call("providers.openai.api_key", "invalid-key")
    mock_config_manager.save.assert_called_once_with(user_level=True)
