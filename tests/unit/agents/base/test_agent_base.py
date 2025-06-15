"""
Unit tests for the agent_base module.
"""

import unittest
from unittest.mock import MagicMock
from typing import Any, Dict

from vaahai.agents.base.agent_base import AgentBase


class TestAgentImplementation(AgentBase):
    """Test implementation of AgentBase for testing."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.initialize_called = False
        super().__init__(config or {})
        
    def initialize(self) -> None:
        self.initialize_called = True
        
    def run(self, *args, **kwargs) -> Any:
        return {"args": args, "kwargs": kwargs}
    
    def cleanup(self) -> None:
        self.cleanup_called = True


class TestAgentBase(unittest.TestCase):
    """Test cases for the AgentBase class."""
    
    def test_initialization(self):
        """Test agent initialization with configuration."""
        config = {"name": "TestAgent", "param1": "value1"}
        agent = TestAgentImplementation(config)
        
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.config, config)
        self.assertTrue(agent.initialize_called)
        
    def test_default_name(self):
        """Test default name when not provided in config."""
        config = {"param1": "value1"}
        agent = TestAgentImplementation(config)
        
        self.assertEqual(agent.name, "TestAgentImplementation")
        
    def test_run_method(self):
        """Test the run method with arguments."""
        agent = TestAgentImplementation()
        result = agent.run("arg1", "arg2", kwarg1="value1")
        
        self.assertEqual(result["args"], ("arg1", "arg2"))
        self.assertEqual(result["kwargs"], {"kwarg1": "value1"})
        
    def test_cleanup_method(self):
        """Test the cleanup method."""
        agent = TestAgentImplementation()
        agent.cleanup()
        
        self.assertTrue(hasattr(agent, "cleanup_called"))
        self.assertTrue(agent.cleanup_called)


if __name__ == "__main__":
    unittest.main()
