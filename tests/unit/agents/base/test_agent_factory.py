"""
Unit tests for the agent factory.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import yaml

from vaahai.agents.base.agent_factory import AgentFactory
from vaahai.agents.base.agent_registry import AgentRegistry


class TestAgentFactory(unittest.TestCase):
    """Test cases for the AgentFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock agent class
        self.mock_agent_class = MagicMock()
        self.mock_agent_instance = MagicMock()
        self.mock_agent_class.return_value = self.mock_agent_instance
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        
        # Register the mock agent class
        self.patcher = patch.object(
            AgentRegistry, 
            "get_agent_class", 
            return_value=self.mock_agent_class
        )
        self.mock_get_agent_class = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        
        # Mock the validate_and_prepare_config method
        self.config_patcher = patch(
            "vaahai.agents.config_loader.AgentConfigLoader.validate_and_prepare_config",
            side_effect=lambda agent_type, config: {"type": agent_type, **(config or {})}
        )
        self.mock_validate_config = self.config_patcher.start()
        self.addCleanup(self.config_patcher.stop)
        
        # Mock the list_agent_types method
        self.list_patcher = patch.object(
            AgentRegistry,
            "list_agent_types",
            return_value=["hello_world", "code_executor"]
        )
        self.mock_list_agent_types = self.list_patcher.start()
        self.addCleanup(self.list_patcher.stop)
        
        # Mock the is_registered method
        self.is_registered_patcher = patch.object(
            AgentRegistry,
            "is_registered",
            side_effect=lambda agent_type: agent_type in ["hello_world", "code_executor"]
        )
        self.mock_is_registered = self.is_registered_patcher.start()
        self.addCleanup(self.is_registered_patcher.stop)
    
    def test_create_agent(self):
        """Test creating an agent."""
        # Create an agent
        config = {"name": "test_agent"}
        agent = AgentFactory.create_agent("hello_world", config)
        
        # Verify that the agent class was called with the correct configuration
        self.mock_validate_config.assert_called_once_with("hello_world", config)
        self.mock_agent_class.assert_called_once()
        self.assertEqual(agent, self.mock_agent_instance)
    
    def test_create_agent_with_no_config(self):
        """Test creating an agent with no configuration."""
        # Create an agent with no configuration
        agent = AgentFactory.create_agent("hello_world")
        
        # Verify that the agent class was called with an empty configuration
        self.mock_validate_config.assert_called_once_with("hello_world", None)
        self.mock_agent_class.assert_called_once()
        self.assertEqual(agent, self.mock_agent_instance)
    
    def test_create_agent_unknown_type(self):
        """Test creating an agent with an unknown type."""
        # Mock the get_agent_class method to return None
        self.mock_get_agent_class.return_value = None
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError) as context:
            AgentFactory.create_agent("unknown_type")
        
        # Verify the error message
        self.assertIn("Unknown agent type: unknown_type", str(context.exception))
    
    def test_create_agent_validation_error(self):
        """Test creating an agent with an invalid configuration."""
        # Mock the validate_and_prepare_config method to raise a ValueError
        self.mock_validate_config.side_effect = ValueError("Invalid configuration")
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError) as context:
            AgentFactory.create_agent("hello_world", {"invalid": "config"})
        
        # Verify the error message
        self.assertIn("Failed to create agent of type hello_world", str(context.exception))
        self.assertIn("Invalid configuration", str(context.exception))
    
    def test_create_agents(self):
        """Test creating multiple agents."""
        # Create a configuration for multiple agents
        agent_configs = {
            "agent1": {"type": "hello_world", "name": "Agent 1"},
            "agent2": {"type": "code_executor", "name": "Agent 2"}
        }
        
        # Create the agents
        agents = AgentFactory.create_agents(agent_configs)
        
        # Verify that the agent classes were called with the correct configurations
        self.assertEqual(self.mock_validate_config.call_count, 2)
        self.assertEqual(self.mock_agent_class.call_count, 2)
        self.assertEqual(len(agents), 2)
        self.assertIn("agent1", agents)
        self.assertIn("agent2", agents)
    
    def test_create_agents_missing_type(self):
        """Test creating multiple agents with a missing type."""
        # Create a configuration with a missing type
        agent_configs = {
            "agent1": {"type": "hello_world", "name": "Agent 1"},
            "agent2": {"name": "Agent 2"}
        }
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError) as context:
            AgentFactory.create_agents(agent_configs)
        
        # Verify the error message
        self.assertIn("Failed to create one or more agents", str(context.exception))
        self.assertIn("Missing agent type for agent2", str(context.exception))
    
    def test_create_agents_validation_error(self):
        """Test creating multiple agents with an invalid configuration."""
        # Create a configuration with an invalid agent
        agent_configs = {
            "agent1": {"type": "hello_world", "name": "Agent 1"},
            "agent2": {"type": "code_executor", "invalid": "config"}
        }
        
        # Mock the validate_and_prepare_config method to raise a ValueError for the second agent
        original_side_effect = self.mock_validate_config.side_effect
        
        def side_effect(agent_type, config):
            if agent_type == "code_executor" and "invalid" in config:
                raise ValueError("Invalid configuration")
            return {"type": agent_type, **(config or {})}
        
        self.mock_validate_config.side_effect = side_effect
        
        # Verify that an exception is raised
        with self.assertRaises(ValueError) as context:
            AgentFactory.create_agents(agent_configs)
        
        # Verify the error message
        self.assertIn("Failed to create one or more agents", str(context.exception))
        self.assertIn("Error creating agent agent2", str(context.exception))
        self.assertIn("Invalid configuration", str(context.exception))
        
        # Restore the original side effect
        self.mock_validate_config.side_effect = original_side_effect
    
    def test_create_agents_from_file_yaml(self):
        """Test creating agents from a YAML file."""
        # Create a test YAML file
        agent_configs = {
            "agent1": {"type": "hello_world", "name": "Agent 1"},
            "agent2": {"type": "code_executor", "name": "Agent 2"}
        }
        
        file_path = Path(self.temp_dir.name) / "agents.yaml"
        with open(file_path, "w") as f:
            yaml.dump(agent_configs, f)
        
        # Create the agents
        with patch("vaahai.agents.config_loader.AgentConfigLoader.load_from_file", return_value=agent_configs):
            agents = AgentFactory.create_agents_from_file(str(file_path))
        
        # Verify that the agents were created
        self.assertEqual(len(agents), 2)
        self.assertIn("agent1", agents)
        self.assertIn("agent2", agents)
    
    def test_create_agents_from_file_error(self):
        """Test creating agents from a file with an error."""
        # Create a test file path
        file_path = Path(self.temp_dir.name) / "agents.yaml"
        
        # Mock the load_from_file method to raise an exception
        with patch("vaahai.agents.config_loader.AgentConfigLoader.load_from_file", side_effect=ValueError("Invalid file")):
            # Verify that an exception is raised
            with self.assertRaises(ValueError) as context:
                AgentFactory.create_agents_from_file(str(file_path))
            
            # Verify the error message
            self.assertIn(f"Failed to create agents from file {file_path}", str(context.exception))
            self.assertIn("Invalid file", str(context.exception))
    
    def test_list_available_agents(self):
        """Test listing available agents."""
        # List available agents
        agents = AgentFactory.list_available_agents()
        
        # Verify that the correct agents are returned
        self.assertEqual(agents, ["hello_world", "code_executor"])
    
    def test_is_agent_available(self):
        """Test checking if an agent is available."""
        # Check if agents are available
        self.assertTrue(AgentFactory.is_agent_available("hello_world"))
        self.assertTrue(AgentFactory.is_agent_available("code_executor"))
        self.assertFalse(AgentFactory.is_agent_available("unknown_type"))
    
    def test_get_agent_metadata(self):
        """Test getting agent metadata."""
        # Create a mock agent class with metadata
        mock_agent_class = MagicMock()
        mock_agent_class.__name__ = "HelloWorldAgent"
        mock_agent_class.__doc__ = "A test agent for saying hello."
        mock_agent_class.metadata = {
            "name": "Hello World Agent",
            "description": "An agent that says hello to the world.",
            "type": "hello_world",
            "capabilities": ["greeting", "introduction"]
        }
        
        # Mock the get_agent_class method to return the mock agent class
        self.mock_get_agent_class.return_value = mock_agent_class
        
        # Get the agent metadata
        metadata = AgentFactory.get_agent_metadata("hello_world")
        
        # Verify that the correct metadata is returned
        self.assertEqual(metadata, mock_agent_class.metadata)
    
    def test_get_agent_metadata_no_metadata(self):
        """Test getting agent metadata when no metadata is defined."""
        # Create a mock agent class without metadata
        mock_agent_class = MagicMock()
        mock_agent_class.__name__ = "HelloWorldAgent"
        mock_agent_class.__doc__ = "A test agent for saying hello."
        mock_agent_class.metadata = {}
        
        # Mock the get_agent_class method to return the mock agent class
        self.mock_get_agent_class.return_value = mock_agent_class
        
        # Get the agent metadata
        metadata = AgentFactory.get_agent_metadata("hello_world")
        
        # Verify that the metadata is generated from the class information
        expected_metadata = {
            "name": "HelloWorldAgent",
            "description": "A test agent for saying hello.",
            "type": "hello_world"
        }
        
        self.assertEqual(metadata, expected_metadata)
    
    def test_get_agent_metadata_no_doc(self):
        """Test getting agent metadata when no docstring is defined."""
        # Create a mock agent class without a docstring
        mock_agent_class = MagicMock()
        mock_agent_class.__name__ = "HelloWorldAgent"
        mock_agent_class.__doc__ = None
        mock_agent_class.metadata = {}
        
        # Mock the get_agent_class method to return the mock agent class
        self.mock_get_agent_class.return_value = mock_agent_class
        
        # Get the agent metadata
        metadata = AgentFactory.get_agent_metadata("hello_world")
        
        # Verify that the metadata is generated from the class information
        expected_metadata = {
            "name": "HelloWorldAgent",
            "description": "No description available",
            "type": "hello_world"
        }
        
        self.assertEqual(metadata, expected_metadata)
    
    def test_get_agent_metadata_unknown_type(self):
        """Test getting metadata for an unknown agent type."""
        # Mock the get_agent_class method to return None
        self.mock_get_agent_class.return_value = None
        
        # Get the agent metadata
        metadata = AgentFactory.get_agent_metadata("unknown_type")
        
        # Verify that None is returned
        self.assertIsNone(metadata)


if __name__ == "__main__":
    unittest.main()
