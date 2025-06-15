"""
Unit tests for the agent_registry module.
"""

import unittest
from typing import Any, Dict

from vaahai.agents.base.agent_base import AgentBase
from vaahai.agents.base.agent_registry import AgentRegistry


class TestAgentOne(AgentBase):
    """Test agent implementation for registry testing."""
    
    def __init__(self):
        """Initialize without calling parent constructor to avoid pytest warning."""
        # Skip parent constructor to avoid pytest collection warning
        pass
    
    def run(self, *args, **kwargs) -> Any:
        return "Agent One"


class TestAgentTwo(AgentBase):
    """Another test agent implementation for registry testing."""
    
    def __init__(self):
        """Initialize without calling parent constructor to avoid pytest warning."""
        # Skip parent constructor to avoid pytest collection warning
        pass
    
    def run(self, *args, **kwargs) -> Any:
        return "Agent Two"


class TestAgentRegistry(unittest.TestCase):
    """Test cases for the AgentRegistry class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Clear the registry before each test
        AgentRegistry._registry = {}
    
    def test_register_decorator(self):
        """Test registering agents using the decorator."""
        
        @AgentRegistry.register("test_agent_one")
        class DecoratedAgent(AgentBase):
            def run(self, *args, **kwargs) -> Any:
                return "Decorated Agent"
        
        self.assertTrue(AgentRegistry.is_registered("test_agent_one"))
        agent_class = AgentRegistry.get_agent_class("test_agent_one")
        self.assertEqual(agent_class, DecoratedAgent)
    
    def test_get_agent_class(self):
        """Test getting agent classes from the registry."""
        
        @AgentRegistry.register("agent_one")
        class _(TestAgentOne):
            pass
        
        @AgentRegistry.register("agent_two")
        class _(TestAgentTwo):
            pass
        
        agent_class_one = AgentRegistry.get_agent_class("agent_one")
        agent_class_two = AgentRegistry.get_agent_class("agent_two")
        
        self.assertEqual(agent_class_one.__base__, TestAgentOne)
        self.assertEqual(agent_class_two.__base__, TestAgentTwo)
        
        # Test getting a non-existent agent class
        self.assertIsNone(AgentRegistry.get_agent_class("non_existent"))
    
    def test_list_agent_types(self):
        """Test listing all registered agent types."""
        
        @AgentRegistry.register("agent_one")
        class _(TestAgentOne):
            pass
        
        @AgentRegistry.register("agent_two")
        class _(TestAgentTwo):
            pass
        
        agent_types = AgentRegistry.list_agent_types()
        
        self.assertEqual(len(agent_types), 2)
        self.assertIn("agent_one", agent_types)
        self.assertIn("agent_two", agent_types)
    
    def test_is_registered(self):
        """Test checking if an agent type is registered."""
        
        @AgentRegistry.register("agent_one")
        class _(TestAgentOne):
            pass
        
        self.assertTrue(AgentRegistry.is_registered("agent_one"))
        self.assertFalse(AgentRegistry.is_registered("non_existent"))


if __name__ == "__main__":
    unittest.main()
