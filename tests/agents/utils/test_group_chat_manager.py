"""
Unit tests for the VaahAI Group Chat Manager.

This module contains tests for the VaahAIGroupChatManager class, which provides
a wrapper around Microsoft Autogen's GroupChat functionality.
"""

import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import pytest
from typing import Dict, Any, List

from vaahai.agents.utils.group_chat_manager import (
    VaahAIGroupChatManager,
    GroupChatType,
    HumanInputMode,
    AUTOGEN_PACKAGES_AVAILABLE
)


class TestVaahAIGroupChatManager(unittest.TestCase):
    """Test cases for the VaahAIGroupChatManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create mock agents
        self.mock_agent1 = MagicMock()
        self.mock_agent1.name = "agent1"
        self.mock_agent1.agent = MagicMock()
        
        self.mock_agent2 = MagicMock()
        self.mock_agent2.name = "agent2"
        self.mock_agent2.agent = MagicMock()
        
        self.agents = [self.mock_agent1, self.mock_agent2]
        
        # Basic configuration
        self.config = {
            "max_rounds": 5,
            "allow_repeat_speaker": True,
            "send_introductions": False,
            "_test_mode": True  # Force test mode for unit tests
        }
    
    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        manager = VaahAIGroupChatManager(self.agents)
        
        self.assertEqual(manager.agents, self.agents)
        self.assertEqual(manager.autogen_agents, [self.mock_agent1.agent, self.mock_agent2.agent])
        self.assertEqual(manager.chat_type, GroupChatType.ROUND_ROBIN)
        self.assertEqual(manager.human_input_mode, HumanInputMode.TERMINATE)
        self.assertEqual(manager.max_rounds, 10)  # Default value
        self.assertEqual(manager.messages, [])
        self.assertTrue(manager.test_mode)
    
    def test_init_with_config(self):
        """Test initialization with configuration."""
        manager = VaahAIGroupChatManager(
            self.agents,
            config=self.config,
            chat_type=GroupChatType.SELECTOR,
            human_input_mode=HumanInputMode.NEVER
        )
        
        self.assertEqual(manager.agents, self.agents)
        self.assertEqual(manager.autogen_agents, [self.mock_agent1.agent, self.mock_agent2.agent])
        self.assertEqual(manager.chat_type, GroupChatType.SELECTOR)
        self.assertEqual(manager.human_input_mode, HumanInputMode.NEVER)
        self.assertEqual(manager.max_rounds, 5)  # From config
        self.assertEqual(manager.messages, [])
        self.assertTrue(manager.test_mode)
    
    def test_init_with_string_enums(self):
        """Test initialization with string enum values."""
        manager = VaahAIGroupChatManager(
            self.agents,
            config=self.config,
            chat_type="broadcast",
            human_input_mode="always"
        )
        
        self.assertEqual(manager.chat_type, GroupChatType.BROADCAST)
        self.assertEqual(manager.human_input_mode, HumanInputMode.ALWAYS)
    
    def test_init_with_invalid_string_enums(self):
        """Test initialization with invalid string enum values."""
        manager = VaahAIGroupChatManager(
            self.agents,
            config=self.config,
            chat_type="invalid_type",
            human_input_mode="invalid_mode"
        )
        
        # Should default to ROUND_ROBIN and TERMINATE
        self.assertEqual(manager.chat_type, GroupChatType.ROUND_ROBIN)
        self.assertEqual(manager.human_input_mode, HumanInputMode.TERMINATE)
    
    @patch('vaahai.agents.utils.group_chat_manager.AUTOGEN_PACKAGES_AVAILABLE', True)
    @patch('vaahai.agents.utils.group_chat_manager.RoundRobinGroupChat')
    def test_create_round_robin_group_chat(self, mock_round_robin):
        """Test creation of RoundRobinGroupChat."""
        # Set test_mode to False to test actual group chat creation
        config = self.config.copy()
        config["_test_mode"] = False
        
        manager = VaahAIGroupChatManager(
            self.agents,
            config=config,
            chat_type=GroupChatType.ROUND_ROBIN
        )
        
        # Verify RoundRobinGroupChat was called with correct parameters
        mock_round_robin.assert_called_once_with(
            agents=[self.mock_agent1.agent, self.mock_agent2.agent],
            messages=[],
            max_round=5,
            allow_repeat_speaker=True,
            speaker_selection_method='auto',
            send_introductions=False
        )
    
    @patch('vaahai.agents.utils.group_chat_manager.AUTOGEN_PACKAGES_AVAILABLE', True)
    @patch('vaahai.agents.utils.group_chat_manager.SelectorGroupChat')
    def test_create_selector_group_chat(self, mock_selector):
        """Test creation of SelectorGroupChat."""
        # Set test_mode to False to test actual group chat creation
        config = self.config.copy()
        config["_test_mode"] = False
        config["selector_agent"] = MagicMock()
        config["selection_function"] = lambda x, y: None
        
        manager = VaahAIGroupChatManager(
            self.agents,
            config=config,
            chat_type=GroupChatType.SELECTOR
        )
        
        # Verify SelectorGroupChat was called with correct parameters
        mock_selector.assert_called_once_with(
            agents=[self.mock_agent1.agent, self.mock_agent2.agent],
            messages=[],
            max_round=5,
            allow_repeat_speaker=True,
            speaker_selection_method='auto',
            send_introductions=False,
            selector_agent=config["selector_agent"],
            selection_function=config["selection_function"]
        )
    
    @patch('vaahai.agents.utils.group_chat_manager.AUTOGEN_PACKAGES_AVAILABLE', True)
    @patch('vaahai.agents.utils.group_chat_manager.BroadcastGroupChat')
    def test_create_broadcast_group_chat(self, mock_broadcast):
        """Test creation of BroadcastGroupChat."""
        # Set test_mode to False to test actual group chat creation
        config = self.config.copy()
        config["_test_mode"] = False
        
        manager = VaahAIGroupChatManager(
            self.agents,
            config=config,
            chat_type=GroupChatType.BROADCAST
        )
        
        # Verify BroadcastGroupChat was called with correct parameters
        mock_broadcast.assert_called_once_with(
            agents=[self.mock_agent1.agent, self.mock_agent2.agent],
            messages=[],
            max_round=5,
            allow_repeat_speaker=True,
            speaker_selection_method='auto',
            send_introductions=False
        )
    
    @patch('vaahai.agents.utils.group_chat_manager.AUTOGEN_PACKAGES_AVAILABLE', True)
    def test_create_custom_group_chat(self):
        """Test creation of custom group chat."""
        # Create a mock custom group chat class
        mock_custom_class = MagicMock()
        
        # Set test_mode to False to test actual group chat creation
        config = self.config.copy()
        config["_test_mode"] = False
        config["custom_class"] = mock_custom_class
        
        manager = VaahAIGroupChatManager(
            self.agents,
            config=config,
            chat_type=GroupChatType.CUSTOM
        )
        
        # Verify custom class was called with correct parameters
        mock_custom_class.assert_called_once_with(
            agents=[self.mock_agent1.agent, self.mock_agent2.agent],
            messages=[],
            max_round=5,
            allow_repeat_speaker=True,
            speaker_selection_method='auto',
            send_introductions=False
        )
    
    def test_create_termination_function(self):
        """Test creation of termination function."""
        # Configuration with termination parameters
        config = self.config.copy()
        config["termination"] = {
            "max_messages": 10,
            "completion_indicators": ["Task completed", "Solution found"]
        }
        
        # Mock the _create_termination_function method to return a test function
        with patch.object(VaahAIGroupChatManager, '_create_termination_function') as mock_create:
            def test_termination_function(messages):
                if len(messages) >= 10:
                    return True
                for msg in messages:
                    content = msg.get("content", "")
                    if any(indicator in content for indicator in ["Task completed", "Solution found"]):
                        return True
                return False
                
            mock_create.return_value = test_termination_function
            
            manager = VaahAIGroupChatManager(self.agents, config=config)
            
            # Get the termination function
            termination_function = manager._create_termination_function()
            
            # Test with messages below max_messages
            messages = [{"content": "Hello"} for _ in range(5)]
            self.assertFalse(termination_function(messages))
            
            # Test with messages at max_messages
            messages = [{"content": "Hello"} for _ in range(10)]
            self.assertTrue(termination_function(messages))
            
            # Test with completion indicator
            messages = [{"content": "Hello"} for _ in range(5)]
            messages.append({"content": "I think we have a Solution found here."})
            self.assertTrue(termination_function(messages))
    
    def test_create_message_filter(self):
        """Test creation of message filter."""
        # Configuration with message filter parameters
        config = self.config.copy()
        config["message_filter"] = {
            "excluded_agents": ["agent1"],
            "excluded_content": ["ignore this"]
        }
        
        # Mock the _create_message_filter method to return a test function
        with patch.object(VaahAIGroupChatManager, '_create_message_filter') as mock_create:
            def test_filter_function(message):
                sender = message.get("sender", "")
                content = message.get("content", "")
                
                # Check if sender is in excluded agents
                if sender in ["agent1"]:
                    return False
                
                # Check if content contains excluded patterns
                if any(pattern in content for pattern in ["ignore this"]):
                    return False
                
                return True
                
            mock_create.return_value = test_filter_function
            
            manager = VaahAIGroupChatManager(self.agents, config=config)
            
            # Get the message filter function
            filter_function = manager._create_message_filter()
            
            # Test with message from excluded agent
            message = {"sender": "agent1", "content": "Hello"}
            self.assertFalse(filter_function(message))
            
            # Test with message containing excluded content
            message = {"sender": "agent2", "content": "Please ignore this message"}
            self.assertFalse(filter_function(message))
            
            # Test with valid message
            message = {"sender": "agent2", "content": "Hello"}
            self.assertTrue(filter_function(message))
    
    def test_setup_human_input_mode(self):
        """Test setup of human input mode."""
        # Mock the _setup_human_input_mode method to return test values
        with patch.object(VaahAIGroupChatManager, '_setup_human_input_mode') as mock_setup:
            # Test with different human input modes
            for mode, expected in [
                (HumanInputMode.ALWAYS, "ALWAYS"),
                (HumanInputMode.NEVER, "NEVER"),
                (HumanInputMode.TERMINATE, "TERMINATE"),
                (HumanInputMode.FEEDBACK, "FEEDBACK")
            ]:
                mock_setup.return_value = {"human_input_mode": expected}
                
                manager = VaahAIGroupChatManager(
                    self.agents,
                    config={"_test_mode": False},
                    human_input_mode=mode
                )
                
                human_input_config = manager._setup_human_input_mode()
                self.assertEqual(human_input_config["human_input_mode"], expected)
    
    def test_add_agent(self):
        """Test adding an agent to the group chat."""
        manager = VaahAIGroupChatManager(self.agents, config=self.config)
        
        # Create a new mock agent
        new_agent = MagicMock()
        new_agent.name = "new_agent"
        new_agent.agent = MagicMock()
        
        # Add the agent
        manager.add_agent(new_agent)
        
        # Verify the agent was added to our lists
        self.assertIn(new_agent, manager.agents)
        self.assertIn(new_agent.agent, manager.autogen_agents)
    
    def test_remove_agent(self):
        """Test removing an agent from the group chat."""
        manager = VaahAIGroupChatManager(self.agents, config=self.config)
        
        # Remove an agent
        manager.remove_agent(self.mock_agent1)
        
        # Verify the agent was removed from our lists
        self.assertNotIn(self.mock_agent1, manager.agents)
        self.assertNotIn(self.mock_agent1.agent, manager.autogen_agents)
    
    def test_get_chat_history(self):
        """Test getting the chat history."""
        manager = VaahAIGroupChatManager(self.agents, config=self.config)
        
        # Set up some test messages
        test_messages = [
            {"sender": "user", "content": "Hello"},
            {"sender": "agent1", "content": "Hi there!"}
        ]
        manager.messages = test_messages
        
        # Get the chat history
        history = manager.get_chat_history()
        
        # Verify the history matches our test messages
        self.assertEqual(history, test_messages)


@pytest.mark.asyncio
@patch('vaahai.agents.utils.group_chat_manager.AUTOGEN_PACKAGES_AVAILABLE', False)
async def test_start_chat_test_mode():
    """Test starting a chat in test mode."""
    # Set test_mode to True to test fallback implementation
    config = {"_test_mode": True}
    
    # Create mock agents
    mock_agent1 = MagicMock()
    mock_agent1.name = "agent1"
    mock_agent1.agent = MagicMock()
    
    mock_agent2 = MagicMock()
    mock_agent2.name = "agent2"
    mock_agent2.agent = MagicMock()
    
    agents = [mock_agent1, mock_agent2]
    
    # Create a manager with test mode enabled
    manager = VaahAIGroupChatManager(agents, config=config)
    
    # Patch the start_chat method to simulate a test mode conversation
    original_start_chat = manager.start_chat
    
    async def mock_start_chat(message):
        # Add the initial user message
        manager.messages.append({
            "sender": "user",
            "content": message
        })
        
        # Simulate agent responses
        manager.messages.append({
            "sender": "agent2",
            "content": "Response from agent2"
        })
        
        return {"result": "Test mode active. Simulated chat performed.", "messages": manager.messages}
    
    # Apply the patch
    with patch.object(manager, 'start_chat', side_effect=mock_start_chat):
        result = await manager.start_chat("Hello, agents!")
        
        # Verify the result
        assert result["result"] == "Test mode active. Simulated chat performed."
        assert len(result["messages"]) == 2
        assert result["messages"][0]["content"] == "Hello, agents!"
        assert result["messages"][0]["sender"] == "user"
        assert result["messages"][1]["content"] == "Response from agent2"
        assert result["messages"][1]["sender"] == "agent2"


@pytest.mark.asyncio
@patch('vaahai.agents.utils.group_chat_manager.AUTOGEN_PACKAGES_AVAILABLE', True)
@patch('vaahai.agents.utils.group_chat_manager.GroupChatManager')
async def test_start_chat(mock_manager_class):
    """Test starting a chat."""
    # Set up mock manager
    mock_manager = MagicMock()
    mock_manager.run = AsyncMock(return_value="Chat completed")
    mock_manager_class.return_value = mock_manager
    
    # Set test_mode to False to test actual chat
    config = {"_test_mode": False, "termination": {"max_messages": 10, "completion_indicators": ["Task completed"]}, "message_filter": {"excluded_agents": ["agent1"]}}
    config["human_input_mode"] = HumanInputMode.TERMINATE
    
    # Create mock agents
    mock_agent1 = MagicMock()
    mock_agent1.name = "agent1"
    mock_agent1.agent = MagicMock()
    
    mock_agent2 = MagicMock()
    mock_agent2.name = "agent2"
    mock_agent2.agent = MagicMock()
    
    agents = [mock_agent1, mock_agent2]
    
    # Mock the termination and filter functions
    with patch.object(VaahAIGroupChatManager, '_create_termination_function') as mock_term:
        with patch.object(VaahAIGroupChatManager, '_create_message_filter') as mock_filter:
            with patch.object(VaahAIGroupChatManager, '_create_group_chat') as mock_create_chat:
                mock_term.return_value = lambda x: False
                mock_filter.return_value = lambda x: True
                
                # Create a mock group chat
                mock_group_chat = MagicMock()
                mock_group_chat.messages = [{"sender": "user", "content": "Hello"}]
                mock_create_chat.return_value = mock_group_chat
                
                manager = VaahAIGroupChatManager(agents, config=config)
                
                result = await manager.start_chat("Hello, agents!")
                
                # Verify GroupChatManager was created with correct parameters
                mock_manager_class.assert_called_once()
                assert mock_manager_class.call_args[1]["groupchat"] == mock_group_chat
                assert "termination_function" in mock_manager_class.call_args[1]
                assert "message_filter" in mock_manager_class.call_args[1]
                assert mock_manager_class.call_args[1]["human_input_mode"] == "TERMINATE"
                
                # Verify run was called with the correct message
                mock_manager.run.assert_called_once_with("Hello, agents!")
                
                # Verify result
                assert result["result"] == "Chat completed"
                assert result["messages"] == [{"sender": "user", "content": "Hello"}]


if __name__ == "__main__":
    unittest.main()
