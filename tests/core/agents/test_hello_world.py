"""
Tests for the Hello World agent.
"""

import pytest
from unittest.mock import patch, MagicMock
from vaahai.core.agents.hello_world import HelloWorldAgent
from vaahai.core.agents.factory import AgentFactory


@patch('autogen.AssistantAgent')
@patch('autogen.UserProxyAgent')
def test_hello_world_agent_default_message(mock_user_proxy, mock_assistant):
    """Test that the Hello World agent returns the default message with Autogen."""
    # Set up mocks
    mock_instance = mock_assistant.return_value
    mock_instance.name = "hello_world_agent"
    
    mock_user_instance = mock_user_proxy.return_value
    mock_user_instance.chat_messages = {
        "hello_world_agent": [{"content": "Hello, World!"}]
    }
    
    # Create and run agent
    agent = HelloWorldAgent()
    result = agent.run()
    
    # Verify results
    assert result["success"] is True
    assert result["message"] == "Hello, World!"
    assert result["agent_type"] == "hello_world"
    
    # Verify Autogen was used correctly
    mock_assistant.assert_called_once()
    mock_user_proxy.assert_called_once()
    mock_user_instance.initiate_chat.assert_called_once()


@patch('autogen.AssistantAgent')
@patch('autogen.UserProxyAgent')
def test_hello_world_agent_custom_message(mock_user_proxy, mock_assistant):
    """Test that the Hello World agent returns a custom message using Autogen."""
    # Set up mocks
    mock_instance = mock_assistant.return_value
    mock_instance.name = "hello_world_agent"
    
    mock_user_instance = mock_user_proxy.return_value
    mock_user_instance.chat_messages = {
        "hello_world_agent": [{"content": "Custom message"}]
    }
    
    # Create and run agent
    agent = HelloWorldAgent({"message": "Custom message"})
    result = agent.run()
    
    # Verify results
    assert result["success"] is True
    assert result["message"] == "Custom message"
    assert result["agent_type"] == "hello_world"
    
    # Verify Autogen was used correctly with custom message
    mock_assistant.assert_called_once()
    system_message = mock_assistant.call_args[1].get('system_message')
    assert "Custom message" in system_message


@patch('autogen.AssistantAgent')
@patch('autogen.UserProxyAgent')
def test_agent_factory_creates_hello_world_agent(mock_user_proxy, mock_assistant):
    """Test that the agent factory creates a Hello World agent using Autogen."""
    # Set up mocks
    mock_instance = mock_assistant.return_value
    mock_instance.name = "hello_world_agent"
    
    mock_user_instance = mock_user_proxy.return_value
    mock_user_instance.chat_messages = {
        "hello_world_agent": [{"content": "Hello, World!"}]
    }
    
    # Create agent through factory
    agent = AgentFactory.create_agent("hello_world")
    
    # Verify agent type
    assert isinstance(agent, HelloWorldAgent)
    
    # Run agent and verify results
    result = agent.run()
    assert result["success"] is True
    assert result["message"] == "Hello, World!"


def test_agent_factory_raises_error_for_unknown_agent():
    """Test that the agent factory raises an error for unknown agent types."""
    with pytest.raises(ValueError):
        AgentFactory.create_agent("unknown_agent_type")


@patch('autogen.AssistantAgent')
@patch('autogen.UserProxyAgent')
def test_hello_world_agent_handles_errors(mock_user_proxy, mock_assistant):
    """Test that the Hello World agent handles errors gracefully."""
    # Set up mocks to raise an exception
    mock_user_instance = mock_user_proxy.return_value
    mock_user_instance.initiate_chat.side_effect = Exception("Test error")
    
    # Create and run agent
    agent = HelloWorldAgent()
    result = agent.run()
    
    # Verify error handling
    assert result["success"] is False
    assert "Error: Test error" in result["message"]
    assert result["agent_type"] == "hello_world"
