"""
Unit tests for the autogen_agent_base module.
"""

import unittest
from unittest.mock import MagicMock, patch
from typing import Any, Dict

# Mock the autogen import before importing AutoGenAgentBase
with patch.dict('sys.modules', {'autogen': MagicMock()}):
    from vaahai.agents.base.autogen_agent_base import AutoGenAgentBase


class TestAutoGenAgentImplementation(AutoGenAgentBase):
    """Test implementation of AutoGenAgentBase for testing."""
    
    def _create_autogen_agent(self) -> Any:
        """Create a mock AutoGen agent for testing."""
        mock_agent = MagicMock()
        mock_agent.chat_history = []
        mock_agent.update_system_message = MagicMock()
        return mock_agent
    
    def run(self, *args, **kwargs) -> Any:
        """Implement the required run method from AgentBase."""
        return {"status": "success", "message": "Test run completed"}


class TestAutoGenAgentBase(unittest.TestCase):
    """Test cases for the AutoGenAgentBase class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock ConfigManager to avoid actual config loading
        self.config_manager_patcher = patch('vaahai.agents.base.autogen_agent_base.ConfigManager')
        self.mock_config_manager = self.config_manager_patcher.start()
        mock_instance = MagicMock()
        mock_instance.get.return_value = {"api_key": "test-api-key", "default_model": "gpt-4"}
        self.mock_config_manager.return_value = mock_instance
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.config_manager_patcher.stop()
    
    def test_initialization(self):
        """Test agent initialization with configuration."""
        config = {"name": "TestAgent", "provider": "openai", "temperature": 0.5}
        agent = TestAutoGenAgentImplementation(config)
        
        self.assertEqual(agent.name, "TestAgent")
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
    
    def test_update_system_message(self):
        """Test updating the system message."""
        agent = TestAutoGenAgentImplementation({})
        agent.update_system_message("New system message")
        
        agent.agent.update_system_message.assert_called_once_with("New system message")
    
    def test_get_conversation_history(self):
        """Test getting the conversation history."""
        agent = TestAutoGenAgentImplementation({})
        agent.agent.chat_history = [{"role": "user", "content": "Hello"}]
        
        history = agent.get_conversation_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["content"], "Hello")


if __name__ == "__main__":
    unittest.main()
