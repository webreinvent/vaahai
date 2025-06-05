"""
VaahAI Agent Architecture Examples

This module provides simple examples of how to use the VaahAI agent architecture
in an MVP context. These examples demonstrate the core functionality while
showcasing the reusability and extensibility of the architecture.
"""

import asyncio
from typing import Dict, Any, List, Optional

from .interfaces import IAgent, IGroupChat, ITool
from .base import BaseAgent, BaseGroupChat, BaseTool
from .adapters import AdapterFactory
from .factory import FactoryProvider
from .config import ConfigFactory


class SimpleAgent(BaseAgent):
    """
    A simple agent implementation for demonstration purposes.
    
    This agent responds to messages with predefined responses based on keywords.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new simple agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name)
        self._responses: Dict[str, str] = {}
    
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check for required configuration
        if "responses" not in self._config:
            return False
        
        # Store responses for quick lookup
        self._responses = self._config["responses"]
        return True
    
    def _initialize_capabilities(self) -> None:
        """Initialize the agent's capabilities."""
        self.add_capability("text_response")
        
        # Add additional capabilities based on configuration
        additional_capabilities = self._config.get("capabilities", [])
        for capability in additional_capabilities:
            self.add_capability(capability)
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and return a response.
        
        Args:
            message: The message to process
            
        Returns:
            The agent's response message
        """
        content = message.get("content", "").lower()
        
        # Find a matching response
        response_content = "I don't know how to respond to that."
        for keyword, response in self._responses.items():
            if keyword.lower() in content:
                response_content = response
                break
        
        return {
            "type": "message",
            "content": response_content,
            "sender_id": self.get_id(),
            "sender_role": "assistant",
            "recipient_id": message.get("sender_id", "user"),
            "metadata": {
                "agent_name": self.get_name(),
                "capabilities": self.get_capabilities()
            }
        }


class SimpleGroupChat(BaseGroupChat):
    """
    A simple group chat implementation for demonstration purposes.
    
    This group chat routes messages in a round-robin fashion.
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize a new simple group chat.
        
        Args:
            name: Name of this group chat. If not provided, the class name will be used.
        """
        super().__init__(name)
        self._current_agent_index = 0
        self._max_rounds = 10
        self._current_round = 0
    
    async def start_chat(self, initial_message: Dict[str, Any]) -> None:
        """
        Start a group chat with an initial message.
        
        Args:
            initial_message: The message to start the chat with
        """
        self._current_round = 0
        self._current_agent_index = 0
        self.add_to_history(initial_message)
        
        # Process the initial message
        await self._process_next_message(initial_message)
    
    async def _process_next_message(self, message: Dict[str, Any]) -> None:
        """
        Process the next message in the chat.
        
        Args:
            message: The message to process
        """
        # Check if we've reached the maximum number of rounds
        if self._current_round >= self._max_rounds:
            return
        
        # Get the next agent
        agents = self.get_agents()
        if not agents:
            return
        
        agent = agents[self._current_agent_index]
        self._current_agent_index = (self._current_agent_index + 1) % len(agents)
        
        # Process the message
        response = await agent.process_message(message)
        self.add_to_history(response)
        
        # Increment the round counter if we've gone through all agents
        if self._current_agent_index == 0:
            self._current_round += 1
        
        # Continue the conversation if we haven't reached the maximum number of rounds
        if self._current_round < self._max_rounds:
            await self._process_next_message(response)
    
    async def end_chat(self) -> Dict[str, Any]:
        """
        End the current group chat.
        
        Returns:
            Summary of the chat
        """
        return {
            "type": "summary",
            "rounds": self._current_round,
            "messages": len(self._history),
            "agents": [agent.get_name() for agent in self.get_agents()]
        }


class SimpleTool(BaseTool):
    """
    A simple tool implementation for demonstration purposes.
    
    This tool performs basic arithmetic operations.
    """
    
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize a new simple tool.
        
        Args:
            name: Name of this tool. If not provided, the class name will be used.
            description: Description of what this tool does.
        """
        super().__init__(name or "Calculator", description or "Performs basic arithmetic operations")
        
        # Define parameters
        self.add_parameter("operation", {
            "type": "string",
            "description": "Operation to perform (add, subtract, multiply, divide)",
            "required": True
        })
        self.add_parameter("a", {
            "type": "number",
            "description": "First operand",
            "required": True
        })
        self.add_parameter("b", {
            "type": "number",
            "description": "Second operand",
            "required": True
        })
    
    async def execute(self, parameters: Dict[str, Any]) -> Any:
        """
        Execute the tool with the given parameters.
        
        Args:
            parameters: Tool execution parameters
            
        Returns:
            Tool execution result
            
        Raises:
            ValueError: If the operation is invalid or parameters are missing
        """
        # Validate parameters
        operation = parameters.get("operation")
        a = parameters.get("a")
        b = parameters.get("b")
        
        if not operation or a is None or b is None:
            raise ValueError("Missing required parameters")
        
        # Perform the operation
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return a / b
        else:
            raise ValueError(f"Invalid operation: {operation}")


async def run_simple_example():
    """
    Run a simple example of the VaahAI agent architecture.
    
    This example creates two agents, adds them to a group chat, and starts a conversation.
    """
    # Create agent factory
    agent_factory = FactoryProvider.get_agent_factory()
    
    # Register agent classes
    agent_factory.register_agent_class("simple", SimpleAgent)
    
    # Create agents
    assistant_config = ConfigFactory.create_config("agent", 
        name="Assistant",
        type="simple",
        responses={
            "hello": "Hello! How can I help you today?",
            "help": "I can assist with various tasks. What do you need help with?",
            "bye": "Goodbye! Have a great day!"
        },
        capabilities=["greeting", "help", "farewell"]
    )
    
    coder_config = ConfigFactory.create_config("agent",
        name="Coder",
        type="simple",
        responses={
            "code": "Here's a simple Python function:\n\ndef hello_world():\n    print('Hello, World!')",
            "function": "Functions are reusable blocks of code that perform a specific task.",
            "bug": "Have you tried turning it off and on again?"
        },
        capabilities=["coding", "debugging", "explanation"]
    )
    
    assistant = agent_factory.create_agent("simple", assistant_config.to_dict())
    coder = agent_factory.create_agent("simple", coder_config.to_dict())
    
    # Create group chat factory
    group_chat_factory = FactoryProvider.get_group_chat_factory()
    
    # Register group chat classes
    group_chat_factory.register_group_chat_class("simple", SimpleGroupChat)
    
    # Create group chat
    group_chat_config = ConfigFactory.create_config("group_chat",
        type="simple",
        name="SimpleChat",
        max_rounds=5
    )
    
    group_chat = group_chat_factory.create_group_chat("simple", group_chat_config.to_dict())
    
    # Add agents to group chat
    group_chat.add_agent(assistant)
    group_chat.add_agent(coder)
    
    # Start the chat
    initial_message = {
        "type": "message",
        "content": "Hello! Can you help me with some code?",
        "sender_id": "user",
        "sender_role": "user",
        "recipient_id": None,
        "metadata": {}
    }
    
    await group_chat.start_chat(initial_message)
    
    # End the chat
    summary = await group_chat.end_chat()
    
    # Print chat history
    print("\nChat History:")
    for i, message in enumerate(group_chat.get_chat_history()):
        sender = message.get("sender_id", "Unknown")
        content = message.get("content", "")
        print(f"{i+1}. {sender}: {content}")
    
    print("\nChat Summary:")
    print(f"Rounds: {summary['rounds']}")
    print(f"Messages: {summary['messages']}")
    print(f"Agents: {', '.join(summary['agents'])}")


async def run_autogen_integration_example():
    """
    Run an example of integrating with Autogen using adapters.
    
    This example demonstrates how to use the adapter pattern to integrate
    VaahAI agents with Autogen.
    """
    # Create agent factory
    agent_factory = FactoryProvider.get_agent_factory()
    
    # Register agent classes
    agent_factory.register_agent_class("simple", SimpleAgent)
    
    # Create a VaahAI agent
    agent_config = ConfigFactory.create_config("agent", 
        name="Assistant",
        type="simple",
        responses={
            "hello": "Hello! How can I help you today?",
            "help": "I can assist with various tasks. What do you need help with?",
            "bye": "Goodbye! Have a great day!"
        },
        capabilities=["greeting", "help", "farewell"]
    )
    
    vaah_agent = agent_factory.create_agent("simple", agent_config.to_dict())
    
    # Create an adapter for Autogen
    adapter_config = ConfigFactory.create_config("adapter",
        framework="autogen",
        agent_type="assistant",
        agent_config={
            "name": vaah_agent.get_name(),
            "llm_config": {
                "model": "gpt-4"
            }
        }
    )
    
    adapter = AdapterFactory.create_agent_adapter("autogen", adapter_config.to_dict())
    
    # Adapt the VaahAI agent to Autogen
    autogen_agent = adapter.adapt_agent(vaah_agent)
    
    # In a real implementation, we would use the Autogen agent here
    # For this example, we'll just print the adapted agent
    print("\nAutogen Integration Example:")
    print(f"Adapted agent: {autogen_agent}")
    
    # Example of message adaptation
    vaah_message = {
        "type": "message",
        "content": "Hello! Can you help me?",
        "sender_id": "user",
        "sender_role": "user",
        "recipient_id": vaah_agent.get_id(),
        "metadata": {}
    }
    
    autogen_message = adapter.adapt_message_to_external(vaah_message)
    print(f"\nVaahAI message: {vaah_message}")
    print(f"Autogen message: {autogen_message}")
    
    # Convert back to VaahAI format
    vaah_message_back = adapter.adapt_message_from_external(autogen_message)
    print(f"Converted back to VaahAI: {vaah_message_back}")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(run_simple_example())
    asyncio.run(run_autogen_integration_example())
