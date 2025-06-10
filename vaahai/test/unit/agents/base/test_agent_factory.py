"""
Unit tests for the agent_factory module.
"""

import unittest
from typing import Any, Dict
from unittest.mock import patch

from vaahai.agents.base.agent_base import AgentBase
from vaahai.agents.base.agent_registry import AgentRegistry
from vaahai.agents.base.agent_factory import AgentFactory


class TestAgentOne(AgentBase):
    """Test agent implementation for factory testing."""
    
    def run(self, *args, **kwargs) -> Any:
        return "Agent One"


class TestAgentTwo(AgentBase):
    """Another test agent implementation for factory testing."""
    
    def run(self, *args, **kwargs) -> Any:
        return "Agent Two"


class TestAgentFactory(unittest.TestCase):
    """Test cases for the AgentFactory class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Clear the registry before each test
        AgentRegistry._registry = {}
        
        # Register test agents
        AgentRegistry._registry["agent_one"] = TestAgentOne
        AgentRegistry._registry["agent_two"] = TestAgentTwo
    
    def test_create_agent(self):
        """Test creating an agent with the factory."""
        config = {"name": "MyAgent", "param1": "value1"}
        agent = AgentFactory.create_agent("agent_one", config)
        
        self.assertIsInstance(agent, TestAgentOne)
        self.assertEqual(agent.name, "MyAgent")
        self.assertEqual(agent.config["param1"], "value1")
    
    def test_create_agent_with_default_config(self):
        """Test creating an agent with default config."""
        agent = AgentFactory.create_agent("agent_one")
        
        self.assertIsInstance(agent, TestAgentOne)
        self.assertEqual(agent.name, "TestAgentOne")
        self.assertEqual(agent.config, {})
    
    def test_create_agent_unknown_type(self):
        """Test creating an agent with an unknown type."""
        with self.assertRaises(ValueError):
            AgentFactory.create_agent("unknown_agent")
    
    def test_create_agents(self):
        """Test creating multiple agents from a configuration dictionary."""
        agent_configs = {
            "agent_a": {"type": "agent_one", "name": "AgentA"},
            "agent_b": {"type": "agent_two", "name": "AgentB"}
        }
        
        agents = AgentFactory.create_agents(agent_configs)
        
        self.assertEqual(len(agents), 2)
        self.assertIn("agent_a", agents)
        self.assertIn("agent_b", agents)
        self.assertIsInstance(agents["agent_a"], TestAgentOne)
        self.assertIsInstance(agents["agent_b"], TestAgentTwo)
        self.assertEqual(agents["agent_a"].name, "AgentA")
        self.assertEqual(agents["agent_b"].name, "AgentB")
    
    def test_create_agents_missing_type(self):
        """Test creating agents with missing type."""
        agent_configs = {
            "agent_a": {"name": "AgentA"}
        }
        
        with self.assertRaises(ValueError):
            AgentFactory.create_agents(agent_configs)
    
    def test_list_available_agents(self):
        """Test listing all available agent types."""
        agent_types = AgentFactory.list_available_agents()
        
        self.assertEqual(len(agent_types), 2)
        self.assertIn("agent_one", agent_types)
        self.assertIn("agent_two", agent_types)
    
    def test_is_agent_available(self):
        """Test checking if an agent type is available."""
        self.assertTrue(AgentFactory.is_agent_available("agent_one"))
        self.assertFalse(AgentFactory.is_agent_available("unknown_agent"))


if __name__ == "__main__":
    unittest.main()
