"""
Unit tests for the model command.
"""

import os
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock, ANY

from vaahai.cli.main import app
from vaahai.config.manager import ConfigManager
from vaahai.config.llm_utils import list_providers, list_models

# Create a test runner
runner = CliRunner()


@pytest.fixture
def mock_config_manager():
    """Create a mock ConfigManager."""
    with patch("vaahai.cli.commands.model.command.ConfigManager") as mock_cm:
        # Create a mock instance
        mock_instance = MagicMock(spec=ConfigManager)
        mock_cm.return_value = mock_instance
        
        # Configure the mock
        mock_instance.get_current_provider.return_value = "openai"
        mock_instance.get_model.return_value = "gpt-4"
        
        # Mock model info
        mock_instance.get_model_info.return_value = {
            "name": "gpt-4",
            "provider": "openai",
            "capabilities": ["text", "code", "function_calling"],
            "context_length": 8192,
            "description": "A powerful language model for various tasks"
        }
        
        yield mock_instance


@pytest.mark.parametrize("command", [
    ["model", "list"],
])
def test_model_list_command(command, mock_config_manager):
    """Test the model list command."""
    with patch("vaahai.cli.commands.model.command.list_providers") as mock_list_providers, \
         patch("vaahai.cli.commands.model.command.list_models") as mock_list_models:
        
        # Configure mocks
        mock_list_providers.return_value = ["openai", "claude"]
        mock_list_models.return_value = ["gpt-4", "gpt-3.5-turbo"]
        
        # Run the command
        result = runner.invoke(app, command)
        
        # Check the result
        assert result.exit_code == 0
        assert "OPENAI Models" in result.stdout
        
        # Verify that the functions were called
        mock_list_providers.assert_called_once()
        # Don't assert exact call count since it may be called multiple times
        assert mock_list_models.called


def test_model_help_command():
    """Test the model command without subcommand shows help."""
    # Run the command
    result = runner.invoke(app, ["model"])
    
    # Check the result
    assert result.exit_code == 0
    assert "vaahai model" in result.stdout
    assert "Subcommands" in result.stdout
    assert "capabilities" in result.stdout
    assert "list" in result.stdout
    assert "info" in result.stdout
    assert "set" in result.stdout
    assert "recommend" in result.stdout


def test_model_list_with_provider(mock_config_manager):
    """Test the model list command with provider filter."""
    with patch("vaahai.cli.commands.model.command.list_providers") as mock_list_providers, \
         patch("vaahai.cli.commands.model.command.list_models") as mock_list_models:
        
        # Configure mocks
        mock_list_providers.return_value = ["openai", "claude"]
        mock_list_models.return_value = ["gpt-4", "gpt-3.5-turbo"]
        
        # Run the command
        result = runner.invoke(app, ["model", "list", "--provider", "openai"])
        
        # Check the result
        assert result.exit_code == 0
        assert "OPENAI Models" in result.stdout
        assert "CLAUDE Models" not in result.stdout
        
        # Verify that the functions were called
        mock_list_providers.assert_called_once()
        # Don't assert exact call count, just check that it was called with the right provider
        mock_list_models.assert_any_call("openai")


def test_model_list_with_capability(mock_config_manager):
    """Test the model list command with capability filter."""
    with patch("vaahai.cli.commands.model.command.list_providers") as mock_list_providers, \
         patch("vaahai.cli.commands.model.command.list_models") as mock_list_models:
        
        # Configure mocks
        mock_list_providers.return_value = ["openai", "claude"]
        mock_list_models.return_value = ["gpt-4", "gpt-3.5-turbo"]
        mock_config_manager.filter_models_by_capability.return_value = ["gpt-4"]
        
        # Run the command
        result = runner.invoke(app, ["model", "list", "--capability", "vision"])
        
        # Check the result
        assert result.exit_code == 0
        
        # Verify that the filter function was called with any provider
        # The implementation may call it with multiple providers
        mock_config_manager.filter_models_by_capability.assert_called()


def test_model_info_command(mock_config_manager):
    """Test the model info command."""
    # Run the command
    result = runner.invoke(app, ["model", "info"])
    
    # Check the result
    assert result.exit_code == 0
    assert "gpt-4" in result.stdout
    assert "8,192 tokens" in result.stdout
    
    # Verify that the functions were called
    mock_config_manager.get_model_info.assert_called_once()


def test_model_info_with_model(mock_config_manager):
    """Test the model info command with a specific model."""
    # Run the command
    result = runner.invoke(app, ["model", "info", "gpt-4"])
    
    # Check the result
    assert result.exit_code == 0
    assert "gpt-4" in result.stdout
    
    # Verify that the functions were called
    mock_config_manager.get_model_info.assert_called_once()


def test_model_set_command(mock_config_manager):
    """Test the model set command."""
    # Run the command
    result = runner.invoke(app, ["model", "set", "gpt-4"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Set model to gpt-4" in result.stdout
    
    # Verify that the functions were called
    mock_config_manager.set_model.assert_called_once_with("gpt-4", "openai")
    mock_config_manager.save.assert_called_once()


def test_model_set_no_save(mock_config_manager):
    """Test the model set command with --no-save."""
    # Run the command
    result = runner.invoke(app, ["model", "set", "gpt-4", "--no-save"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Set model to gpt-4" in result.stdout
    assert "not saved" in result.stdout
    
    # Verify that the functions were called
    mock_config_manager.set_model.assert_called_once_with("gpt-4", "openai")
    mock_config_manager.save.assert_not_called()


def test_model_recommend_command(mock_config_manager):
    """Test the model recommend command."""
    # Configure the mock
    mock_config_manager.get_recommended_model.return_value = "gpt-4"
    
    # Run the command
    result = runner.invoke(app, ["model", "recommend", "--capability", "code"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Recommended model" in result.stdout
    assert "gpt-4" in result.stdout
    
    # Verify that the functions were called
    mock_config_manager.get_recommended_model.assert_called_once()
    mock_config_manager.get_model_info.assert_called_once()


def test_model_recommend_with_set(mock_config_manager):
    """Test the model recommend command with --set."""
    # Configure the mock
    mock_config_manager.get_recommended_model.return_value = "gpt-4"
    
    # Run the command
    result = runner.invoke(app, ["model", "recommend", "--capability", "code", "--set"])
    
    # Check the result
    assert result.exit_code == 0
    assert "Recommended model" in result.stdout
    assert "Set model to gpt-4" in result.stdout
    
    # Verify that the functions were called
    mock_config_manager.get_recommended_model.assert_called_once()
    mock_config_manager.set_model.assert_called_once_with("gpt-4", "openai")


def test_model_capabilities_command(mock_config_manager):
    """Test the model capabilities command."""
    with patch("vaahai.cli.commands.model.command.get_all_capabilities") as mock_get_all_capabilities, \
         patch("vaahai.cli.commands.model.command.get_providers_with_capability") as mock_get_providers:
        
        # Configure mocks
        mock_get_all_capabilities.return_value = ["text", "code", "vision"]
        mock_get_providers.return_value = ["openai", "claude"]
        
        # Run the command
        result = runner.invoke(app, ["model", "capabilities"])
        
        # Check the result
        assert result.exit_code == 0
        assert "Available Model Capabilities" in result.stdout
        assert "text" in result.stdout
        assert "code" in result.stdout
        assert "vision" in result.stdout
        
        # Verify that the functions were called
        mock_get_all_capabilities.assert_called_once()
        assert mock_get_providers.call_count > 0


def test_model_capabilities_with_capability(mock_config_manager):
    """Test the model capabilities command with a specific capability."""
    with patch("vaahai.cli.commands.model.command.get_providers_with_capability") as mock_get_providers:
        
        # Configure mocks
        mock_get_providers.return_value = ["openai", "claude"]
        mock_config_manager.filter_models_by_capability.return_value = ["gpt-4"]
        
        # Run the command
        result = runner.invoke(app, ["model", "capabilities", "--capability", "vision"])
        
        # Check the result
        assert result.exit_code == 0
        assert "Models with vision capability" in result.stdout
        
        # Verify that the functions were called
        mock_get_providers.assert_called_once_with("vision")
        # The implementation may call filter_models_by_capability with any provider
        mock_config_manager.filter_models_by_capability.assert_called()
