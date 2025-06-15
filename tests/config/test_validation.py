"""
Tests for the VaahAI configuration validation utility.
"""

import os
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

from vaahai.config.validation import (
    validate_configuration_exists,
    validate_configuration_complete,
    validate_for_command,
    validate_provider_setup,
    check_model_capabilities,
    get_validation_summary
)
from vaahai.config.manager import ConfigManager


class TestConfigValidation(unittest.TestCase):
    """Test cases for the configuration validation utility."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test config
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        
        # Patch environment variable to use our test config directory
        self.env_patcher = patch.dict(os.environ, {"VAAHAI_CONFIG_DIR": str(self.config_dir)})
        self.env_patcher.start()

    def tearDown(self):
        """Clean up test environment."""
        self.env_patcher.stop()
        self.temp_dir.cleanup()

    @patch('vaahai.config.validation.ConfigManager')
    def test_validate_configuration_exists_not_found(self, mock_config_manager):
        """Test validation when configuration doesn't exist."""
        # Mock the ConfigManager
        mock_instance = MagicMock()
        mock_config_manager.return_value = mock_instance
        mock_instance.exists.return_value = False
        
        exists, message = validate_configuration_exists()
        self.assertFalse(exists)
        self.assertIn("not found", message)

    def test_validate_configuration_exists_found(self):
        """Test validation when configuration exists."""
        # Create a minimal config file
        config_path = self.config_dir / "config.toml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            f.write('[llm]\nprovider = "openai"\n')
        
        exists, message = validate_configuration_exists()
        self.assertTrue(exists)
        self.assertEqual(message, "Configuration exists")

    def test_validate_provider_setup_missing_api_key(self):
        """Test validation of provider setup with missing API key."""
        config = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "model": "gpt-4"
                }
            }
        }
        
        errors = validate_provider_setup(config, "openai")
        self.assertIn("Missing API key for openai", errors)

    def test_validate_provider_setup_invalid_model(self):
        """Test validation of provider setup with invalid model."""
        config = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "api_key": "test-key",
                    "model": "nonexistent-model"
                }
            }
        }
        
        errors = validate_provider_setup(config, "openai")
        self.assertIn("Invalid model 'nonexistent-model' for openai", errors)

    def test_validate_provider_setup_valid(self):
        """Test validation of provider setup with valid configuration."""
        config = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "api_key": "test-key",
                    "model": "gpt-4"
                }
            }
        }
        
        errors = validate_provider_setup(config, "openai")
        self.assertEqual(len(errors), 0)

    def test_check_model_capabilities_missing(self):
        """Test checking model capabilities with missing capabilities."""
        valid, missing = check_model_capabilities(
            "openai", "gpt-3.5-turbo", ["vision"]
        )
        self.assertFalse(valid)
        self.assertIn("vision", missing)

    def test_check_model_capabilities_valid(self):
        """Test checking model capabilities with valid capabilities."""
        valid, missing = check_model_capabilities(
            "openai", "gpt-4", ["text", "code"]
        )
        self.assertTrue(valid)
        self.assertEqual(len(missing), 0)

    @patch('vaahai.config.validation.ConfigManager')
    def test_validate_configuration_complete_errors(self, mock_config_manager):
        """Test complete configuration validation with errors."""
        # Mock the ConfigManager
        mock_instance = MagicMock()
        mock_config_manager.return_value = mock_instance
        mock_instance.exists.return_value = True
        
        # Mock the configuration
        mock_instance.get_full_config.return_value = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "model": "nonexistent-model"
                }
            }
        }
        
        errors = validate_configuration_complete()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("API key" in error for error in errors))
        self.assertTrue(any("Invalid model" in error for error in errors))

    @patch('vaahai.config.validation.validate_configuration_complete')
    @patch('vaahai.config.validation.ConfigManager')
    def test_validate_for_command_review(self, mock_config_manager, mock_validate_complete):
        """Test validation for review command."""
        # Mock validate_configuration_complete to return no errors
        mock_validate_complete.return_value = []
        
        # Mock the ConfigManager
        mock_instance = MagicMock()
        mock_config_manager.return_value = mock_instance
        
        # Mock the configuration with a model that supports code
        mock_instance.get_full_config.return_value = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "api_key": "test-key",
                    "model": "gpt-4"
                }
            }
        }
        
        valid, errors = validate_for_command("review")
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
        
        # Now test with a model that doesn't exist
        mock_instance.get_full_config.return_value = {
            "llm": {
                "provider": "openai",
                "openai": {
                    "api_key": "test-key",
                    "model": "nonexistent-model"
                }
            }
        }
        
        valid, errors = validate_for_command("review")
        self.assertFalse(valid)
        self.assertTrue(any("Unknown model" in error for error in errors))

    @patch('vaahai.config.validation.validate_configuration_exists')
    @patch('vaahai.config.validation.validate_configuration_complete')
    def test_get_validation_summary(self, mock_validate_complete, mock_validate_exists):
        """Test getting validation summary."""
        # Mock validation results
        mock_validate_exists.return_value = (True, "Configuration exists")
        mock_validate_complete.return_value = ["Error 1", "Error 2"]
        
        # Mock ConfigManager
        with patch('vaahai.config.validation.ConfigManager') as mock_config_manager:
            mock_instance = MagicMock()
            mock_config_manager.return_value = mock_instance
            mock_instance.get_current_provider.return_value = "openai"
            mock_instance.get_model.return_value = "gpt-4"
            
            summary = get_validation_summary()
            
            self.assertFalse(summary["is_valid"])
            self.assertTrue(summary["exists"])
            self.assertEqual(len(summary["errors"]), 2)
            self.assertEqual(summary["provider"], "openai")
            self.assertEqual(summary["model"], "gpt-4")
            self.assertEqual(summary["error_count"], 2)


if __name__ == "__main__":
    unittest.main()
