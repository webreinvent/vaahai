"""
Unit tests for the agent configuration loader.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from vaahai.agents.config_loader import AgentConfigLoader
from vaahai.agents.schemas import get_default_config


class TestAgentConfigLoader(unittest.TestCase):
    """Test cases for the AgentConfigLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
    
    def test_load_from_file_yaml(self):
        """Test loading configuration from a YAML file."""
        # Create a test YAML file
        config = {
            "name": "test_agent",
            "type": "hello_world",
            "llm_config": {
                "model": "gpt-4"
            }
        }
        
        file_path = Path(self.temp_dir.name) / "test_config.yaml"
        with open(file_path, "w") as f:
            yaml.dump(config, f)
        
        # Load the configuration
        loaded_config = AgentConfigLoader.load_from_file(file_path)
        
        # Verify the loaded configuration
        self.assertEqual(loaded_config, config)
    
    def test_load_from_file_json(self):
        """Test loading configuration from a JSON file."""
        # Create a test JSON file
        config = {
            "name": "test_agent",
            "type": "hello_world",
            "llm_config": {
                "model": "gpt-4"
            }
        }
        
        file_path = Path(self.temp_dir.name) / "test_config.json"
        with open(file_path, "w") as f:
            json.dump(config, f)
        
        # Load the configuration
        loaded_config = AgentConfigLoader.load_from_file(file_path)
        
        # Verify the loaded configuration
        self.assertEqual(loaded_config, config)
    
    def test_load_from_file_not_found(self):
        """Test loading configuration from a non-existent file."""
        file_path = Path(self.temp_dir.name) / "non_existent.yaml"
        
        # Verify that an exception is raised
        with self.assertRaises(FileNotFoundError):
            AgentConfigLoader.load_from_file(file_path)
    
    def test_load_from_file_invalid_yaml(self):
        """Test loading configuration from an invalid YAML file."""
        # Create an invalid YAML file
        file_path = Path(self.temp_dir.name) / "invalid.yaml"
        with open(file_path, "w") as f:
            f.write("invalid: yaml: content: - : - :")
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError):
            AgentConfigLoader.load_from_file(file_path)
    
    def test_load_from_file_invalid_json(self):
        """Test loading configuration from an invalid JSON file."""
        # Create an invalid JSON file
        file_path = Path(self.temp_dir.name) / "invalid.json"
        with open(file_path, "w") as f:
            f.write("{invalid: json}")
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError):
            AgentConfigLoader.load_from_file(file_path)
    
    def test_load_from_file_unsupported_format(self):
        """Test loading configuration from a file with an unsupported format."""
        # Create a test file with an unsupported extension
        file_path = Path(self.temp_dir.name) / "config.txt"
        with open(file_path, "w") as f:
            f.write("Some text content")
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError):
            AgentConfigLoader.load_from_file(file_path)
    
    def test_process_env_vars(self):
        """Test processing environment variables in configuration."""
        # Create a test configuration with environment variables
        config = {
            "name": "test_agent",
            "api_key": "${API_KEY:default_key}",
            "nested": {
                "value": "${NESTED_VAR:nested_default}"
            },
            "list": ["${LIST_VAR:list_default}", "static_value"]
        }
        
        # Set up environment variables
        with patch.dict(os.environ, {"API_KEY": "test_key", "NESTED_VAR": "nested_value"}):
            # Process environment variables
            processed_config = AgentConfigLoader.process_env_vars(config)
        
        # Verify the processed configuration
        expected_config = {
            "name": "test_agent",
            "api_key": "test_key",
            "nested": {
                "value": "nested_value"
            },
            "list": ["list_default", "static_value"]
        }
        
        self.assertEqual(processed_config, expected_config)
    
    def test_merge_configs(self):
        """Test merging configurations."""
        # Create base and override configurations
        base_config = {
            "name": "base_agent",
            "type": "hello_world",
            "llm_config": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            },
            "base_only": "base_value"
        }
        
        override_config = {
            "name": "override_agent",
            "llm_config": {
                "model": "gpt-4",
                "max_tokens": 1000
            },
            "override_only": "override_value"
        }
        
        # Merge the configurations
        merged_config = AgentConfigLoader.merge_configs(base_config, override_config)
        
        # Verify the merged configuration
        expected_config = {
            "name": "override_agent",
            "type": "hello_world",
            "llm_config": {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "base_only": "base_value",
            "override_only": "override_value"
        }
        
        self.assertEqual(merged_config, expected_config)
    
    def test_prepare_agent_config(self):
        """Test preparing agent configuration."""
        # Create a test configuration
        config = {
            "name": "test_agent",
            "llm_config": {
                "model": "gpt-4"
            }
        }
        
        # Prepare the configuration
        agent_type = "hello_world"
        prepared_config = AgentConfigLoader.prepare_agent_config(agent_type, config)
        
        # Get the default configuration for comparison
        default_config = get_default_config(agent_type)
        default_config["type"] = agent_type
        
        # Verify that the prepared configuration includes defaults and overrides
        self.assertEqual(prepared_config["type"], agent_type)
        self.assertEqual(prepared_config["name"], "test_agent")
        self.assertEqual(prepared_config["llm_config"]["model"], "gpt-4")
        
        # Check that default values are preserved
        for key, value in default_config.items():
            if key not in ["type", "name", "llm_config"]:
                self.assertEqual(prepared_config[key], value)
    
    def test_prepare_agent_config_with_env_vars(self):
        """Test preparing agent configuration with environment variables."""
        # Create a test configuration with environment variables
        config = {
            "name": "test_agent",
            "api_key": "${API_KEY:default_key}"
        }
        
        # Set up environment variables
        with patch.dict(os.environ, {"API_KEY": "test_key"}):
            # Prepare the configuration
            prepared_config = AgentConfigLoader.prepare_agent_config("hello_world", config)
        
        # Verify that environment variables are processed
        self.assertEqual(prepared_config["api_key"], "test_key")
    
    def test_validate_and_prepare_config_valid(self):
        """Test validating and preparing a valid configuration."""
        # Create a valid test configuration
        config = {
            "name": "test_agent",
            "llm_config": {
                "model": "gpt-4"
            }
        }
        
        # Mock the validation function to always return an empty list (no errors)
        with patch("vaahai.agents.schemas.validate_agent_config", return_value=[]):
            # Validate and prepare the configuration
            validated_config = AgentConfigLoader.validate_and_prepare_config("hello_world", config)
        
        # Verify that the configuration is prepared correctly
        self.assertEqual(validated_config["type"], "hello_world")
        self.assertEqual(validated_config["name"], "test_agent")
    
    def test_validate_and_prepare_config_invalid(self):
        """Test validating and preparing an invalid configuration."""
        # Create an invalid test configuration
        config = {
            "name": "test_agent",
            "type": "code_executor"
            # Missing required execution_environment field
        }
        
        # Mock prepare_agent_config to return our invalid config
        with patch.object(AgentConfigLoader, 'prepare_agent_config', return_value=config):
            # Mock validate_agent_config to return validation errors
            validation_errors = ["deque([]): 'execution_environment' is a required property"]
            with patch("vaahai.agents.schemas.validate_agent_config", return_value=validation_errors):
                # Verify that an exception is raised
                with self.assertRaises(ValueError) as context:
                    AgentConfigLoader.validate_and_prepare_config("code_executor", config)
                
                # Verify the error message contains the expected validation errors
                error_message = str(context.exception)
                self.assertIn("Invalid agent configuration for code_executor", error_message)
                self.assertIn("'execution_environment' is a required property", error_message)


if __name__ == "__main__":
    unittest.main()
