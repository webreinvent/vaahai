"""
Unit tests for the GroupChatFactory.
"""

import unittest
from unittest.mock import patch, MagicMock

from vaahai.agents.base.group_chat_factory import GroupChatFactory
from vaahai.agents.utils.group_chat_manager import GroupChatType, HumanInputMode


class TestGroupChatFactory(unittest.TestCase):
    """Test cases for the GroupChatFactory."""

    @patch('vaahai.agents.base.group_chat_factory.AgentFactory')
    @patch('vaahai.agents.base.group_chat_factory.VaahAIGroupChatManager')
    def test_create_group_chat(self, mock_manager, mock_agent_factory):
        """Test creating a group chat with the factory."""
        # Setup mocks
        mock_agent1 = MagicMock()
        mock_agent2 = MagicMock()
        mock_agent_factory.create_agent.side_effect = [mock_agent1, mock_agent2]
        
        # Create agent configs
        agent_configs = [
            {"type": "assistant", "name": "Assistant"},
            {"type": "user_proxy", "name": "User"}
        ]
        
        # Create chat config
        chat_config = {
            "type": "round_robin",
            "human_input_mode": "terminate",
            "max_rounds": 5
        }
        
        # Create group chat
        GroupChatFactory.create_group_chat(
            agent_configs=agent_configs,
            chat_config=chat_config
        )
        
        # Verify agent factory calls
        mock_agent_factory.create_agent.assert_any_call("assistant", {"name": "Assistant"})
        mock_agent_factory.create_agent.assert_any_call("user_proxy", {"name": "User"})
        
        # Verify manager creation
        mock_manager.assert_called_once()
        args, kwargs = mock_manager.call_args
        self.assertEqual(len(kwargs["agents"]), 2)
        self.assertEqual(kwargs["config"]["type"], "round_robin")
        self.assertEqual(kwargs["config"]["max_rounds"], 5)

    @patch('vaahai.agents.base.group_chat_factory.AgentFactory')
    @patch('vaahai.agents.base.group_chat_factory.VaahAIGroupChatManager')
    def test_create_round_robin_chat(self, mock_manager, mock_agent_factory):
        """Test creating a round robin chat with the factory."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_agent_factory.create_agent.return_value = mock_agent
        
        # Create agent configs
        agent_configs = [
            {"type": "assistant", "name": "Assistant"}
        ]
        
        # Create group chat
        GroupChatFactory.create_round_robin_chat(
            agent_configs=agent_configs,
            human_input_mode=HumanInputMode.NEVER
        )
        
        # Verify manager creation
        mock_manager.assert_called_once()
        args, kwargs = mock_manager.call_args
        self.assertEqual(kwargs["config"]["type"], "round_robin")
        self.assertEqual(kwargs["config"]["human_input_mode"], "never")

    @patch('vaahai.agents.base.group_chat_factory.AgentFactory')
    @patch('vaahai.agents.base.group_chat_factory.VaahAIGroupChatManager')
    def test_create_selector_chat(self, mock_manager, mock_agent_factory):
        """Test creating a selector chat with the factory."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_agent_factory.create_agent.return_value = mock_agent
        
        # Create agent configs
        agent_configs = [
            {"type": "assistant", "name": "Assistant"}
        ]
        
        # Create group chat
        GroupChatFactory.create_selector_chat(
            agent_configs=agent_configs,
            selector_agent_name="Assistant",
            human_input_mode="always"
        )
        
        # Verify manager creation
        mock_manager.assert_called_once()
        args, kwargs = mock_manager.call_args
        self.assertEqual(kwargs["config"]["type"], "selector")
        self.assertEqual(kwargs["config"]["selector_agent"], "Assistant")
        self.assertEqual(kwargs["config"]["human_input_mode"], "always")

    @patch('vaahai.agents.base.group_chat_factory.AgentFactory')
    @patch('vaahai.agents.base.group_chat_factory.VaahAIGroupChatManager')
    def test_create_broadcast_chat(self, mock_manager, mock_agent_factory):
        """Test creating a broadcast chat with the factory."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_agent_factory.create_agent.return_value = mock_agent
        
        # Create agent configs
        agent_configs = [
            {"type": "assistant", "name": "Assistant"}
        ]
        
        # Create group chat
        GroupChatFactory.create_broadcast_chat(
            agent_configs=agent_configs,
            human_input_mode=HumanInputMode.FEEDBACK
        )
        
        # Verify manager creation
        mock_manager.assert_called_once()
        args, kwargs = mock_manager.call_args
        self.assertEqual(kwargs["config"]["type"], "broadcast")
        self.assertEqual(kwargs["config"]["human_input_mode"], "feedback")

    @patch('vaahai.agents.base.group_chat_factory.AgentFactory')
    @patch('vaahai.agents.base.group_chat_factory.VaahAIGroupChatManager')
    def test_create_custom_chat(self, mock_manager, mock_agent_factory):
        """Test creating a custom chat with the factory."""
        # Setup mocks
        mock_agent = MagicMock()
        mock_agent_factory.create_agent.return_value = mock_agent
        
        # Create agent configs
        agent_configs = [
            {"type": "assistant", "name": "Assistant"}
        ]
        
        # Create group chat
        GroupChatFactory.create_custom_chat(
            agent_configs=agent_configs,
            custom_class="my.custom.ChatClass",
            human_input_mode=HumanInputMode.TERMINATE
        )
        
        # Verify manager creation
        mock_manager.assert_called_once()
        args, kwargs = mock_manager.call_args
        self.assertEqual(kwargs["config"]["type"], "custom")
        self.assertEqual(kwargs["config"]["custom_class"], "my.custom.ChatClass")
        self.assertEqual(kwargs["config"]["human_input_mode"], "terminate")

    @patch('vaahai.agents.base.group_chat_factory.AgentFactory')
    def test_missing_agent_type(self, mock_agent_factory):
        """Test error handling when agent type is missing."""
        # Create agent configs with missing type
        agent_configs = [
            {"name": "Assistant"}
        ]
        
        # Verify error is raised
        with self.assertRaises(ValueError):
            GroupChatFactory.create_group_chat(agent_configs=agent_configs)


if __name__ == "__main__":
    unittest.main()
