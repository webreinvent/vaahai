"""
Tests for the ConfigLoader class.

This module contains tests for the ConfigLoader class, which is responsible for
loading configurations from various sources and validating them against schemas.
"""

import os
import json
import tempfile
import unittest
from unittest.mock import patch

from vaahai.agents.config_loader import (
    ConfigLoader,
    ConfigLoadError,
    ConfigValidationError
)
from vaahai.agents.config import (
    LLMConfig,
    AutogenAgentConfig,
    AutogenGroupChatConfig,
    AutogenToolConfig
)


class TestConfigLoader(unittest.TestCase):
    """Tests for the ConfigLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Valid configurations for testing
        self.valid_llm_config = {
            "model": "gpt-4",
            "api_key": "test-key",
            "api_type": "openai"
        }
        
        self.valid_agent_config = {
            "name": "TestAgent",
            "system_message": "You are a test agent",
            "human_input_mode": "NEVER"
        }
        
        self.valid_group_chat_config = {
            "name": "TestChat",
            "agents": ["agent1", "agent2"],
            "max_round": 10
        }
        
        self.valid_tool_config = {
            "name": "TestTool",
            "description": "A test tool",
            "parameters": {
                "param1": {
                    "type": "string",
                    "description": "A test parameter"
                }
            }
        }
        
        # Complete Autogen configuration for testing
        self.valid_autogen_config = {
            "agents": {
                "agent1": self.valid_agent_config,
                "agent2": {
                    "name": "Agent2",
                    "system_message": "You are agent 2",
                    "human_input_mode": "NEVER"
                }
            },
            "group_chats": {
                "chat1": self.valid_group_chat_config
            },
            "tools": {
                "tool1": self.valid_tool_config
            }
        }
    
    def test_load_from_dict_llm(self):
        """Test loading LLM configuration from a dictionary."""
        config = ConfigLoader.load_from_dict(self.valid_llm_config, "llm")
        self.assertIsInstance(config, LLMConfig)
        self.assertEqual(config.get("model"), "gpt-4")
        self.assertEqual(config.get("api_key"), "test-key")
        self.assertEqual(config.get("api_type"), "openai")
    
    def test_load_from_dict_agent(self):
        """Test loading agent configuration from a dictionary."""
        config = ConfigLoader.load_from_dict(self.valid_agent_config, "autogen_agent")
        self.assertIsInstance(config, AutogenAgentConfig)
        self.assertEqual(config.get("name"), "TestAgent")
        self.assertEqual(config.get("system_message"), "You are a test agent")
        self.assertEqual(config.get("human_input_mode"), "NEVER")
    
    def test_load_from_dict_group_chat(self):
        """Test loading group chat configuration from a dictionary."""
        config = ConfigLoader.load_from_dict(self.valid_group_chat_config, "autogen_group_chat")
        self.assertIsInstance(config, AutogenGroupChatConfig)
        self.assertEqual(config.get("name"), "TestChat")
        self.assertEqual(config.get("agents"), ["agent1", "agent2"])
        self.assertEqual(config.get("max_round"), 10)
    
    def test_load_from_dict_tool(self):
        """Test loading tool configuration from a dictionary."""
        config = ConfigLoader.load_from_dict(self.valid_tool_config, "autogen_tool")
        self.assertIsInstance(config, AutogenToolConfig)
        self.assertEqual(config.get("name"), "TestTool")
        self.assertEqual(config.get("description"), "A test tool")
    
    def test_load_from_dict_invalid(self):
        """Test loading invalid configuration from a dictionary."""
        invalid_config = {"name": "Invalid"}  # Missing required fields
        with self.assertRaises(ConfigValidationError):
            ConfigLoader.load_from_dict(invalid_config, "autogen_agent")
    
    def test_load_from_json_string(self):
        """Test loading configuration from a JSON string."""
        json_string = json.dumps(self.valid_llm_config)
        config = ConfigLoader.load_from_json_string(json_string, "llm")
        self.assertIsInstance(config, LLMConfig)
        self.assertEqual(config.get("model"), "gpt-4")
    
    def test_load_from_json_string_invalid_json(self):
        """Test loading configuration from an invalid JSON string."""
        invalid_json = "{"  # Invalid JSON
        with self.assertRaises(ConfigLoadError):
            ConfigLoader.load_from_json_string(invalid_json, "llm")
    
    def test_load_from_file(self):
        """Test loading configuration from a file."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False) as f:
            json.dump(self.valid_llm_config, f)
            f.flush()
            file_path = f.name
        
        try:
            config = ConfigLoader.load_from_file(file_path, "llm")
            self.assertIsInstance(config, LLMConfig)
            self.assertEqual(config.get("model"), "gpt-4")
        finally:
            os.unlink(file_path)
    
    def test_load_from_file_not_found(self):
        """Test loading configuration from a non-existent file."""
        with self.assertRaises(ConfigLoadError):
            ConfigLoader.load_from_file("/nonexistent/file.json", "llm")
    
    def test_load_from_file_unsupported_format(self):
        """Test loading configuration from a file with unsupported format."""
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w+", delete=False) as f:
            f.write("Not a JSON file")
            f.flush()
            file_path = f.name
        
        try:
            with self.assertRaises(ConfigLoadError):
                ConfigLoader.load_from_file(file_path, "llm")
        finally:
            os.unlink(file_path)
    
    def test_substitute_env_vars(self):
        """Test environment variable substitution."""
        with patch.dict(os.environ, {"API_KEY": "test-env-key", "MODEL": "gpt-4-env"}):
            config = {
                "model": "${MODEL}",
                "api_key": "${API_KEY}",
                "nested": {
                    "value": "${API_KEY}"
                },
                "list": ["${MODEL}", "${API_KEY}"]
            }
            
            result = ConfigLoader.substitute_env_vars(config)
            
            self.assertEqual(result["model"], "gpt-4-env")
            self.assertEqual(result["api_key"], "test-env-key")
            self.assertEqual(result["nested"]["value"], "test-env-key")
            self.assertEqual(result["list"][0], "gpt-4-env")
            self.assertEqual(result["list"][1], "test-env-key")
    
    def test_substitute_env_vars_missing(self):
        """Test substitution of missing environment variables."""
        config = {"api_key": "${NONEXISTENT_VAR}"}
        result = ConfigLoader.substitute_env_vars(config)
        self.assertEqual(result["api_key"], "${NONEXISTENT_VAR}")  # Unchanged
    
    def test_load_autogen_config(self):
        """Test loading a complete Autogen configuration."""
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False) as f:
            json.dump(self.valid_autogen_config, f)
            f.flush()
            file_path = f.name
        
        try:
            config = ConfigLoader.load_autogen_config(file_path)
            
            # Check agents
            self.assertEqual(len(config["agents"]), 2)
            self.assertIn("agent1", config["agents"])
            self.assertIn("agent2", config["agents"])
            self.assertIsInstance(config["agents"]["agent1"], AutogenAgentConfig)
            
            # Check group chats
            self.assertEqual(len(config["group_chats"]), 1)
            self.assertIn("chat1", config["group_chats"])
            self.assertIsInstance(config["group_chats"]["chat1"], AutogenGroupChatConfig)
            
            # Check tools
            self.assertEqual(len(config["tools"]), 1)
            self.assertIn("tool1", config["tools"])
            self.assertIsInstance(config["tools"]["tool1"], AutogenToolConfig)
        finally:
            os.unlink(file_path)
    
    def test_load_autogen_config_with_invalid_component(self):
        """Test loading Autogen configuration with an invalid component."""
        # Create a config with an invalid agent
        invalid_config = self.valid_autogen_config.copy()
        invalid_config["agents"]["invalid_agent"] = {"name": "Invalid"}  # Missing required fields
        
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w+", delete=False) as f:
            json.dump(invalid_config, f)
            f.flush()
            file_path = f.name
        
        try:
            with self.assertRaises(ConfigValidationError) as context:
                ConfigLoader.load_autogen_config(file_path)
            
            # Check that the error message contains the invalid agent name
            self.assertIn("invalid_agent", str(context.exception))
        finally:
            os.unlink(file_path)


if __name__ == "__main__":
    unittest.main()
