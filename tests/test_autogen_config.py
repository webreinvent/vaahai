"""
Test script for VaahAI Autogen configuration schema.

This script tests the Autogen configuration schema implementation,
including validation of agent, group chat, and tool configurations.
"""

import sys
import os
import json
import unittest
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaahai.agents.config import (
    ConfigFactory,
    AutogenAgentConfig,
    AutogenGroupChatConfig,
    AutogenToolConfig,
    LLMConfig
)


class TestAutogenConfigSchema(unittest.TestCase):
    """Test cases for Autogen configuration schema."""
    
    def test_llm_config(self):
        """Test LLM configuration."""
        # Test valid OpenAI configuration
        openai_config = {
            "model": "gpt-4",
            "api_key": "test-key",
            "api_type": "openai",
            "organization": "org-123456",
            "api_rate_limit": 60.0,
            "base_url": "https://api.openai.com/v1"
        }
        llm_config = LLMConfig(**openai_config)
        self.assertTrue(llm_config.validate())
        
        # Test valid Azure OpenAI configuration
        azure_config = {
            "model": "my-gpt-4-deployment",
            "api_key": "test-key",
            "api_type": "azure",
            "base_url": "https://example.openai.azure.com/",
            "api_version": "2024-02-01"
        }
        llm_config = LLMConfig(**azure_config)
        self.assertTrue(llm_config.validate())
        
        # Test valid custom LLM configuration
        custom_config = {
            "model": "llama-7B",
            "api_type": "custom",
            "base_url": "http://localhost:1234"
        }
        llm_config = LLMConfig(**custom_config)
        self.assertTrue(llm_config.validate())
        
        # Test invalid configuration (missing required field)
        invalid_config = {
            "api_key": "test-key",
            "api_type": "openai"
        }
        llm_config = LLMConfig(**invalid_config)
        self.assertFalse(llm_config.validate())
    
    def test_autogen_agent_config(self):
        """Test Autogen agent configuration."""
        # Test valid configuration
        valid_config = {
            "name": "TestAgent",
            "system_message": "You are a helpful assistant.",
            "llm_config": {
                "config_list": [
                    {
                        "model": "gpt-4",
                        "api_key": "test-key"
                    }
                ]
            },
            "human_input_mode": "NEVER"
        }
        agent_config = AutogenAgentConfig(**valid_config)
        self.assertTrue(agent_config.validate())
        
        # Test invalid configuration (invalid human_input_mode)
        invalid_config = {
            "name": "TestAgent",
            "system_message": "You are a helpful assistant.",
            "llm_config": {
                "config_list": [
                    {
                        "model": "gpt-4",
                        "api_key": "test-key"
                    }
                ]
            },
            "human_input_mode": "INVALID"
        }
        agent_config = AutogenAgentConfig(**invalid_config)
        self.assertFalse(agent_config.validate())
    
    def test_autogen_group_chat_config(self):
        """Test Autogen group chat configuration."""
        # Test valid configuration
        valid_config = {
            "name": "TestGroupChat",
            "agents": ["agent1", "agent2"],
            "max_round": 10,
            "speaker_selection_method": "round_robin"
        }
        group_chat_config = AutogenGroupChatConfig(**valid_config)
        self.assertTrue(group_chat_config.validate())
        
        # Test invalid configuration (missing required field)
        invalid_config = {
            "name": "TestGroupChat",
            "max_round": 10
        }
        group_chat_config = AutogenGroupChatConfig(**invalid_config)
        self.assertFalse(group_chat_config.validate())
    
    def test_autogen_tool_config(self):
        """Test Autogen tool configuration."""
        # Test valid configuration
        valid_config = {
            "name": "TestTool",
            "description": "A test tool",
            "parameters": {
                "param1": {
                    "type": "string",
                    "description": "A test parameter"
                }
            }
        }
        tool_config = AutogenToolConfig(**valid_config)
        self.assertTrue(tool_config.validate())
        
        # Test invalid configuration (missing required field)
        invalid_config = {
            "name": "TestTool",
            "parameters": {}
        }
        tool_config = AutogenToolConfig(**invalid_config)
        self.assertFalse(tool_config.validate())
    
    def test_config_factory(self):
        """Test configuration factory."""
        # Create agent config
        agent_config = ConfigFactory.from_dict("autogen_agent", {
            "name": "TestAgent",
            "system_message": "You are a test agent",
            "human_input_mode": "NEVER"
        })
        self.assertIsInstance(agent_config, AutogenAgentConfig)
        self.assertEqual(agent_config.get("name"), "TestAgent")
        
        # Create group chat config
        group_chat_config = ConfigFactory.from_dict("autogen_group_chat", {
            "name": "TestChat",
            "agents": ["agent1", "agent2"],
            "max_round": 10
        })
        self.assertIsInstance(group_chat_config, AutogenGroupChatConfig)
        self.assertEqual(group_chat_config.get("name"), "TestChat")
        
        # Create tool config
        tool_config = ConfigFactory.from_dict("autogen_tool", {
            "name": "TestTool",
            "description": "A test tool",
            "parameters": {
                "param1": {
                    "type": "string",
                    "description": "A test parameter"
                }
            }
        })
        self.assertIsInstance(tool_config, AutogenToolConfig)
        self.assertEqual(tool_config.get("name"), "TestTool")


if __name__ == "__main__":
    print("Testing VaahAI Autogen Configuration Schema")
    print("===========================================")
    unittest.main()
