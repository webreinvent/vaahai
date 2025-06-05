"""
Test script for VaahAI agent architecture.

This script tests the core functionality of the VaahAI agent architecture,
including agents, message processors, group chats, and the factory system.
"""

import asyncio
import sys
import os
from typing import Dict, Any, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaahai.agents import (
    BaseAgent,
    BaseMessageProcessor,
    BaseGroupChat,
    AgentFactory,
    GroupChatFactory,
    FactoryProvider,
    ConfigFactory
)


class TestAgent(BaseAgent):
    """A simple test agent for demonstration purposes."""
    
    def _validate_config(self) -> bool:
        """Validate the agent configuration."""
        return True
    
    def _initialize_capabilities(self) -> None:
        """Initialize the agent's capabilities."""
        self.add_capability("test")
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming message and return a response."""
        content = message.get("content", "")
        response = f"Agent {self.get_name()} received: {content}"
        
        return {
            "type": "message",
            "content": response,
            "sender_id": self.get_id(),
            "sender_role": "assistant",
            "recipient_id": message.get("sender_id", "user"),
            "metadata": {
                "agent_name": self.get_name()
            }
        }


class TestGroupChat(BaseGroupChat):
    """A simple test group chat for demonstration purposes."""
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize a new test group chat.
        
        Args:
            name: Name of this group chat. If not provided, the class name will be used.
        """
        self._name = name or self.__class__.__name__
        self._agents = []
        self._history = []
    
    def get_name(self) -> str:
        """
        Get the name of this group chat.
        
        Returns:
            Group chat name
        """
        return self._name
    
    async def start_chat(self, initial_message: Dict[str, Any]) -> None:
        """Start a group chat with an initial message."""
        self.add_to_history(initial_message)
        
        # Process the message with each agent in sequence
        for agent in self.get_agents():
            response = await agent.process_message(initial_message)
            self.add_to_history(response)
    
    async def end_chat(self) -> Dict[str, Any]:
        """End the current group chat."""
        return {
            "type": "summary",
            "messages": len(self._history),
            "agents": [agent.get_name() for agent in self.get_agents()]
        }
    
    def add_agent(self, agent: BaseAgent) -> None:
        """
        Add an agent to this group chat.
        
        Args:
            agent: Agent to add
        """
        self._agents.append(agent)
    
    def get_agents(self) -> list:
        """
        Get all agents in this group chat.
        
        Returns:
            List of agents
        """
        return self._agents
    
    def add_to_history(self, message: Dict[str, Any]) -> None:
        """
        Add a message to the chat history.
        
        Args:
            message: Message to add
        """
        self._history.append(message)
    
    def get_chat_history(self) -> list:
        """
        Get the chat history.
        
        Returns:
            List of messages
        """
        return self._history


async def run_test():
    """Run a test of the VaahAI agent architecture."""
    print("Testing VaahAI Agent Architecture")
    print("=================================")
    
    # Step 1: Set up factories
    print("\nStep 1: Setting up factories")
    agent_factory = FactoryProvider.get_agent_factory()
    group_chat_factory = FactoryProvider.get_group_chat_factory()
    
    # Register test classes
    agent_factory.register_agent_class("test", TestAgent)
    group_chat_factory.register_group_chat_class("test", TestGroupChat)
    
    print(f"Registered agent types: {agent_factory.list_components()}")
    print(f"Registered group chat types: {group_chat_factory.list_components()}")
    
    # Step 2: Create agents
    print("\nStep 2: Creating agents")
    agent1_config = ConfigFactory.create_config("agent", name="Agent1", type="test")
    agent2_config = ConfigFactory.create_config("agent", name="Agent2", type="test")
    
    agent1 = agent_factory.create_agent("test", agent1_config.to_dict())
    agent2 = agent_factory.create_agent("test", agent2_config.to_dict())
    
    print(f"Created agent: {agent1.get_name()} (ID: {agent1.get_id()})")
    print(f"Created agent: {agent2.get_name()} (ID: {agent2.get_id()})")
    
    # Step 3: Test individual agent message processing
    print("\nStep 3: Testing individual agent message processing")
    test_message = {
        "type": "message",
        "content": "Hello, agent!",
        "sender_id": "user",
        "sender_role": "user",
        "recipient_id": agent1.get_id(),
        "metadata": {}
    }
    
    response1 = await agent1.process_message(test_message)
    print(f"Agent 1 response: {response1['content']}")
    
    response2 = await agent2.process_message(test_message)
    print(f"Agent 2 response: {response2['content']}")
    
    # Step 4: Create and test group chat
    print("\nStep 4: Creating and testing group chat")
    group_chat_config = ConfigFactory.create_config("group_chat", name="TestChat", type="test")
    group_chat = group_chat_factory.create_group_chat("test", group_chat_config.to_dict())
    
    print(f"Created group chat: {group_chat.get_name()}")
    
    # Add agents to group chat
    group_chat.add_agent(agent1)
    group_chat.add_agent(agent2)
    
    print(f"Added agents to group chat: {[agent.get_name() for agent in group_chat.get_agents()]}")
    
    # Start the chat
    initial_message = {
        "type": "message",
        "content": "Hello, group chat!",
        "sender_id": "user",
        "sender_role": "user",
        "recipient_id": None,
        "metadata": {}
    }
    
    await group_chat.start_chat(initial_message)
    
    # Print chat history
    print("\nChat History:")
    for i, message in enumerate(group_chat.get_chat_history()):
        sender = message.get("sender_id", "Unknown")
        content = message.get("content", "")
        print(f"{i+1}. {sender}: {content}")
    
    # End the chat
    summary = await group_chat.end_chat()
    print("\nChat Summary:")
    print(f"Messages: {summary['messages']}")
    print(f"Agents: {', '.join(summary['agents'])}")
    
    print("\nTest completed successfully!")


if __name__ == "__main__":
    asyncio.run(run_test())
