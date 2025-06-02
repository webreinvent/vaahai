"""
Tests for the Hello World agent.
"""

import pytest
from vaahai.core.agents.hello_world import HelloWorldAgent
from vaahai.core.agents.factory import AgentFactory


def test_hello_world_agent_default_message():
    """Test that the Hello World agent returns the default message."""
    agent = HelloWorldAgent()
    result = agent.run()
    
    assert result["success"] is True
    assert result["message"] == "Hello, World!"
    assert result["agent_type"] == "hello_world"


def test_hello_world_agent_custom_message():
    """Test that the Hello World agent returns a custom message."""
    agent = HelloWorldAgent({"message": "Custom message"})
    result = agent.run()
    
    assert result["success"] is True
    assert result["message"] == "Custom message"
    assert result["agent_type"] == "hello_world"


def test_agent_factory_creates_hello_world_agent():
    """Test that the agent factory creates a Hello World agent."""
    agent = AgentFactory.create_agent("hello_world")
    
    assert isinstance(agent, HelloWorldAgent)
    
    result = agent.run()
    assert result["success"] is True
    assert result["message"] == "Hello, World!"


def test_agent_factory_raises_error_for_unknown_agent():
    """Test that the agent factory raises an error for unknown agent types."""
    with pytest.raises(ValueError):
        AgentFactory.create_agent("unknown_agent_type")
