"""
Unit tests for the autogen_agent_base module.
"""

import unittest
import os
from unittest.mock import MagicMock, patch
from typing import Any, Dict

# Mock the autogen_agentchat and autogen_ext imports before importing AutoGenAgentBase
with patch.dict('sys.modules', {
    'autogen_agentchat.agents': MagicMock(),
    'autogen_ext.models': MagicMock(),
    'autogen_ext.models.openai': MagicMock()
}):
    from vaahai.agents.base.autogen_agent_base import AutoGenAgentBase


class TestAutoGenAgentImplementation(AutoGenAgentBase):
    """Test implementation of AutoGenAgentBase for testing."""
    
    def _create_autogen_agent(self) -> Any:
        """Create a mock AutoGen agent for testing."""
        mock_agent = MagicMock()
        return mock_agent
    
    def run(self, *args, **kwargs) -> Any:
        """Implement the required run method from AgentBase."""
        return {"status": "success", "message": "Test run completed"}


class TestAutoGenAgentBase(unittest.TestCase):
    """Test cases for the AutoGenAgentBase class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # We need to patch where the functions are imported and used
        self.config_loader_patcher = patch('vaahai.agents.base.autogen_agent_base.load_config')
        self.mock_load_config = self.config_loader_patcher.start()
        self.mock_load_config.return_value = {"llm": {"api_key": "test-api-key", "model": "gpt-4"}}
        
        self.get_config_value_patcher = patch('vaahai.agents.base.autogen_agent_base.get_config_value')
        self.mock_get_config_value = self.get_config_value_patcher.start()
        self.mock_get_config_value.side_effect = lambda key, config: {
            "llm.api_key": "test-api-key",
            "llm.model": "gpt-4"
        }.get(key)
        
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'OPENAI_API_KEY': 'env-test-key',
            'OPENAI_API_BASE': 'https://api.openai.com/v1'
        })
        self.env_patcher.start()
        
        # Mock model client creation
        self.model_client_patcher = patch('vaahai.agents.base.autogen_agent_base.OpenAIChatCompletionClient')
        self.mock_model_client = self.model_client_patcher.start()
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.config_loader_patcher.stop()
        self.get_config_value_patcher.stop()
        self.env_patcher.stop()
        self.model_client_patcher.stop()
    
    def test_initialization(self):
        """Test agent initialization with configuration."""
        config = {"name": "TestAgent", "provider": "openai", "temperature": 0.5}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.config, config)
        self.assertEqual(agent.llm_config["temperature"], 0.5)
        self.assertEqual(agent.llm_config["api_key"], "test-api-key")
        self.assertEqual(agent.llm_config["model"], "gpt-4")
    
    def test_prepare_llm_config_with_model(self):
        """Test LLM config preparation with specified model."""
        config = {"provider": "openai", "model": "gpt-3.5-turbo"}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.llm_config["model"], "gpt-3.5-turbo")
    
    def test_prepare_llm_config_with_custom_config(self):
        """Test LLM config preparation with custom LLM config."""
        config = {
            "provider": "openai",
            "llm_config": {
                "max_tokens": 1000,
                "top_p": 0.9
            }
        }
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.llm_config["max_tokens"], 1000)
        self.assertEqual(agent.llm_config["top_p"], 0.9)
    
    def test_environment_variable_fallback(self):
        """Test fallback to environment variables for API key."""
        # Mock get_config_value to return None for api_key
        self.mock_get_config_value.side_effect = lambda key, config: None if key == "llm.api_key" else "gpt-4"
        
        config = {"provider": "openai"}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.llm_config["api_key"], "env-test-key")
    
    def test_project_specific_api_key(self):
        """Test handling of project-specific API keys (sk-proj-)."""
        # Mock get_config_value to return a project-specific API key
        self.mock_get_config_value.side_effect = lambda key, config: "sk-proj-abc123" if key == "llm.api_key" else "gpt-4"
        
        config = {"provider": "openai"}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.llm_config["api_key"], "sk-proj-abc123")
        self.assertEqual(agent.llm_config["api_type"], "azure")
    
    def test_api_base_url_from_env(self):
        """Test setting API base URL from environment variables."""
        config = {"provider": "openai"}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.llm_config["api_base"], "https://api.openai.com/v1")
    
    def test_test_mode(self):
        """Test agent creation in test mode."""
        config = {"provider": "openai", "_test_mode": True}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.llm_config["model"], "gpt-3.5-turbo")
        # No API key should be loaded in test mode
        self.assertNotIn("api_key", agent.llm_config)


if __name__ == "__main__":
    unittest.main()
