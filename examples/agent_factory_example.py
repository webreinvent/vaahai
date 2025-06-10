#!/usr/bin/env python3
"""
Example demonstrating the enhanced agent factory with configuration loading and validation.

This example shows how to:
1. Create agents with validated configurations
2. Load agent configurations from files
3. Create multiple agents at once
4. Handle configuration errors
"""

import os
import sys
import tempfile
from pathlib import Path

import yaml

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vaahai.agents.base.agent_factory import AgentFactory
from vaahai.agents.base.agent_registry import AgentRegistry
from vaahai.agents.base.agent_base import AgentBase


# Define a simple test agent class
class HelloWorldAgent(AgentBase):
    """A simple agent that says hello."""
    
    def __init__(self, config):
        super().__init__(config)
        self.greeting = config.get("greeting", "Hello")
        self.target = config.get("target", "World")
    
    def run(self):
        """Run the agent."""
        return f"{self.greeting}, {self.target}!"


# Register the agent with the registry
@AgentRegistry.register("hello_world")
class HelloWorldAgentRegistered(HelloWorldAgent):
    """Registered version of the HelloWorldAgent."""
    pass


def main():
    """Run the example."""
    print("Agent Factory Example")
    print("====================\n")
    
    # Example 1: Create a single agent with a simple configuration
    print("Example 1: Create a single agent")
    print("-------------------------------")
    
    try:
        config = {
            "name": "MyGreeter",
            "greeting": "Hi",
            "target": "VaahAI"
        }
        
        agent = AgentFactory.create_agent("hello_world", config)
        print(f"Created agent: {agent.name}")
        print(f"Agent result: {agent.run()}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n")
    
    # Example 2: Create an agent with environment variables in the configuration
    print("Example 2: Create an agent with environment variables")
    print("--------------------------------------------------")
    
    try:
        # Set an environment variable for the example
        os.environ["GREETING"] = "Howdy"
        
        config = {
            "name": "EnvGreeter",
            "greeting": "${GREETING:Hello}",
            "target": "${TARGET:Partner}"
        }
        
        agent = AgentFactory.create_agent("hello_world", config)
        print(f"Created agent: {agent.name}")
        print(f"Agent result: {agent.run()}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n")
    
    # Example 3: Create multiple agents from a dictionary
    print("Example 3: Create multiple agents")
    print("-------------------------------")
    
    try:
        agent_configs = {
            "agent1": {
                "type": "hello_world",
                "name": "Greeter1",
                "greeting": "Hello"
            },
            "agent2": {
                "type": "hello_world",
                "name": "Greeter2",
                "greeting": "Bonjour",
                "target": "Monde"
            }
        }
        
        agents = AgentFactory.create_agents(agent_configs)
        for name, agent in agents.items():
            print(f"Created agent {name}: {agent.name}")
            print(f"Agent result: {agent.run()}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n")
    
    # Example 4: Create agents from a YAML file
    print("Example 4: Create agents from a file")
    print("---------------------------------")
    
    try:
        # Create a temporary YAML file
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w", delete=False) as temp:
            agent_configs = {
                "file_agent1": {
                    "type": "hello_world",
                    "name": "FileGreeter1",
                    "greeting": "Hola",
                    "target": "Mundo"
                },
                "file_agent2": {
                    "type": "hello_world",
                    "name": "FileGreeter2",
                    "greeting": "Ciao",
                    "target": "Mondo"
                }
            }
            yaml.dump(agent_configs, temp)
            temp_path = temp.name
        
        print(f"Loading agents from file: {temp_path}")
        agents = AgentFactory.create_agents_from_file(temp_path)
        
        for name, agent in agents.items():
            print(f"Created agent {name}: {agent.name}")
            print(f"Agent result: {agent.run()}")
        
        # Clean up the temporary file
        os.unlink(temp_path)
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n")
    
    # Example 5: Handle validation errors
    print("Example 5: Handle validation errors")
    print("--------------------------------")
    
    try:
        # This will fail validation because the type is unknown
        AgentFactory.create_agent("unknown_type", {"name": "BadAgent"})
    except ValueError as e:
        print(f"Expected error for unknown type: {e}")
    
    print("\n")
    
    # Example 6: List available agents and get metadata
    print("Example 6: List available agents and metadata")
    print("-----------------------------------------")
    
    available_agents = AgentFactory.list_available_agents()
    print(f"Available agent types: {available_agents}")
    
    for agent_type in available_agents:
        metadata = AgentFactory.get_agent_metadata(agent_type)
        print(f"\nAgent type: {agent_type}")
        print(f"  Name: {metadata.get('name')}")
        print(f"  Description: {metadata.get('description')}")


if __name__ == "__main__":
    main()
