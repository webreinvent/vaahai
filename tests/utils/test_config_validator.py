"""
Tests for the configuration validation utility.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil

from vaahai.utils.config_validator import ConfigValidator, ValidationLevel, ValidationResult


class TestConfigValidator(unittest.TestCase):
    """Tests for the ConfigValidator class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.user_config_dir = Path(self.temp_dir) / ".vaahai"
        self.project_config_dir = Path(self.temp_dir) / "project" / ".vaahai"
        
        # Create patches for config directory paths
        self.user_dir_patcher = patch('vaahai.utils.config_validator.get_user_config_dir', 
                                      return_value=self.user_config_dir)
        self.project_dir_patcher = patch('vaahai.utils.config_validator.get_project_config_dir', 
                                         return_value=self.project_config_dir)
        
        # Start patches
        self.mock_user_dir = self.user_dir_patcher.start()
        self.mock_project_dir = self.project_dir_patcher.start()
    
    def tearDown(self):
        """Clean up test environment."""
        # End patches
        self.user_dir_patcher.stop()
        self.project_dir_patcher.stop()
        
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_validation_result_string_representation(self):
        """Test the string representation of ValidationResult."""
        # Valid result with key
        valid_result = ValidationResult(
            ValidationLevel.INFO,
            "This is valid",
            key="test.key",
            valid=True,
        )
        self.assertIn("✅", str(valid_result))
        self.assertIn("INFO", str(valid_result))
        self.assertIn("test.key", str(valid_result))
        self.assertIn("This is valid", str(valid_result))
        
        # Invalid result without key
        invalid_result = ValidationResult(
            ValidationLevel.ERROR,
            "This is invalid",
            valid=False,
        )
        self.assertIn("❌", str(invalid_result))
        self.assertIn("ERROR", str(invalid_result))
        self.assertIn("This is invalid", str(invalid_result))
        self.assertNotIn("[", str(invalid_result))  # No key in string
    
    def test_is_configured_with_no_config(self):
        """Test is_configured when no config exists."""
        # No directories exist
        self.assertFalse(ConfigValidator.is_configured())
    
    def test_is_configured_with_dir_no_file(self):
        """Test is_configured when directory exists but no config file."""
        # Create user config directory
        os.makedirs(self.user_config_dir)
        
        # Still should return False (no config file)
        self.assertFalse(ConfigValidator.is_configured())
    
    def test_is_configured_with_complete_config(self):
        """Test is_configured with complete configuration."""
        # Create user config directory and file
        os.makedirs(self.user_config_dir)
        with open(self.user_config_dir / "config.toml", "w") as f:
            f.write("# Valid TOML content")
        
        # Should return True (directory and file exist)
        self.assertTrue(ConfigValidator.is_configured())
    
    @patch('vaahai.utils.config_validator.ConfigManager')
    def test_validate_unconfigured(self, mock_config_manager):
        """Test validate when VaahAI is not configured."""
        # ConfigManager will raise an exception if called
        mock_config_manager.side_effect = Exception("Config not found")
        
        validator = ConfigValidator()
        is_valid, results = validator.validate()
        
        # Validation should fail
        self.assertFalse(is_valid)
        
        # Should contain "not configured" message
        error_messages = [r.message for r in results if not r.valid]
        self.assertTrue(any("not configured" in msg.lower() for msg in error_messages))
        
        # Should have user_config_dir result with valid=False
        self.assertTrue(any(r.key == "user_config_dir" and not r.valid for r in results))
    
    def test_validate_with_user_config_only(self):
        """Test validate with only user config."""
        # Create user config directory and file
        os.makedirs(self.user_config_dir)
        with open(self.user_config_dir / "config.toml", "w") as f:
            f.write("[llm]\nprovider = 'openai'\n\n[llm.openai]\nmodel = 'gpt-4'\napi_key = 'sk-12345'")
        
        # Mock ConfigManager to return specific values
        with patch('vaahai.utils.config_validator.ConfigManager') as mock_cm:
            instance = mock_cm.return_value
            instance.get_current_provider.return_value = "openai"
            instance.get_model.return_value = "gpt-4"
            instance.get_api_key.return_value = "sk-12345"
            
            validator = ConfigValidator()
            is_valid, results = validator.validate()
            
            # Validation should pass
            self.assertTrue(is_valid)
            
            # User config directory and file should be valid
            self.assertTrue(any(r.key == "user_config_dir" and r.valid for r in results))
            self.assertTrue(any(r.key == "user_config_file" and r.valid for r in results))
            
            # Project config should be a warning (not required)
            project_results = [r for r in results if r.key == "project_config_dir"]
            self.assertEqual(len(project_results), 1)
            self.assertEqual(project_results[0].level, ValidationLevel.WARNING)
            self.assertFalse(project_results[0].valid)
            
            # Provider, model, and API key should be valid
            self.assertTrue(any(r.key == "llm.provider" and r.valid for r in results))
            self.assertTrue(any(r.key == "llm.openai.model" and r.valid for r in results))
            self.assertTrue(any(r.key == "llm.openai.api_key" and r.valid for r in results))
    
    def test_validate_with_complete_config(self):
        """Test validate with complete user and project config."""
        # Create user config directory and file
        os.makedirs(self.user_config_dir)
        with open(self.user_config_dir / "config.toml", "w") as f:
            f.write("[llm]\nprovider = 'openai'\n\n[llm.openai]\nmodel = 'gpt-4'\napi_key = 'sk-12345'")
        
        # Create project config directory and file
        os.makedirs(self.project_config_dir, exist_ok=True)
        with open(self.project_config_dir / "config.toml", "w") as f:
            f.write("[llm]\nprovider = 'anthropic'\n\n[llm.anthropic]\nmodel = 'claude-3'\napi_key = 'sk-54321'")
        
        # Mock ConfigManager to return specific values
        with patch('vaahai.utils.config_validator.ConfigManager') as mock_cm:
            instance = mock_cm.return_value
            instance.get_current_provider.return_value = "anthropic"  # Project overrides user
            instance.get_model.return_value = "claude-3"
            instance.get_api_key.return_value = "sk-54321"
            
            validator = ConfigValidator()
            is_valid, results = validator.validate()
            
            # Validation should pass
            self.assertTrue(is_valid)
            
            # Both user and project config should be valid
            self.assertTrue(any(r.key == "user_config_dir" and r.valid for r in results))
            self.assertTrue(any(r.key == "user_config_file" and r.valid for r in results))
            self.assertTrue(any(r.key == "project_config_dir" and r.valid for r in results))
            self.assertTrue(any(r.key == "project_config_file" and r.valid for r in results))
            
            # Provider, model, and API key should reflect project values
            provider_results = [r for r in results if r.key == "llm.provider" and r.valid]
            self.assertEqual(len(provider_results), 1)
            self.assertIn("anthropic", provider_results[0].message)
            
            model_results = [r for r in results if r.key == "llm.anthropic.model" and r.valid]
            self.assertEqual(len(model_results), 1)
            self.assertIn("claude-3", model_results[0].message)
    
    @patch('vaahai.utils.config_validator.ConfigManager')
    def test_validate_with_missing_api_key(self, mock_config_manager):
        """Test validate with missing API key."""
        # Create user config directory and file
        os.makedirs(self.user_config_dir)
        with open(self.user_config_dir / "config.toml", "w") as f:
            f.write("[llm]\nprovider = 'openai'\n\n[llm.openai]\nmodel = 'gpt-4'")
        
        # Mock ConfigManager to return specific values
        instance = mock_config_manager.return_value
        instance.get_current_provider.return_value = "openai"
        instance.get_model.return_value = "gpt-4"
        instance.get_api_key.return_value = ""  # Empty API key
        
        validator = ConfigValidator()
        is_valid, results = validator.validate()
        
        # Validation should fail due to missing API key
        self.assertFalse(is_valid)
        
        # Provider and model should be valid
        self.assertTrue(any(r.key == "llm.provider" and r.valid for r in results))
        self.assertTrue(any(r.key == "llm.openai.model" and r.valid for r in results))
        
        # API key should be invalid
        api_key_results = [r for r in results if r.key == "llm.openai.api_key"]
        self.assertEqual(len(api_key_results), 1)
        self.assertEqual(api_key_results[0].level, ValidationLevel.ERROR)
        self.assertFalse(api_key_results[0].valid)


if __name__ == '__main__':
    unittest.main()
