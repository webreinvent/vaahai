#!/usr/bin/env python3
"""
Example implementation of VaahAI agents using Microsoft AutoGen.

This example demonstrates how to:
1. Create base agent classes
2. Implement specialized agents
3. Set up a group chat
4. Run a simple conversation

Usage:
    python agent_implementation_example.py

Requirements:
    - autogen
    - vaahai
"""

import os
import sys
from typing import Any, Dict, List, Optional, Type

# Mock imports for demonstration purposes
# In a real implementation, these would be actual imports
try:
    import autogen
except ImportError:
    print("This example requires autogen. Install it with: pip install pyautogen")
    sys.exit(1)

try:
    from vaahai.config.manager import ConfigManager
except ImportError:
    print("This example requires vaahai. Install it with: pip install vaahai")
    sys.exit(1)


# Base agent classes
class AgentBase:
    """Abstract base class for all VaahAI agents."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        self.initialize()
    
    def initialize(self) -> None:
        """Initialize agent resources."""
        print(f"Initializing {self.name}")
    
    def run(self, *args, **kwargs) -> Any:
        """Run the agent with the given inputs."""
        raise NotImplementedError("Subclasses must implement run()")
    
    def cleanup(self) -> None:
        """Clean up any resources used by the agent."""
        print(f"Cleaning up {self.name}")


class AutoGenAgentBase(AgentBase):
    """Base class for AutoGen-based agents."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.llm_config = self._prepare_llm_config()
        self.agent = self._create_autogen_agent()
    
    def _prepare_llm_config(self) -> Dict[str, Any]:
        """Prepare the LLM configuration for the agent."""
        # Get API key from environment or config
        api_key = os.environ.get("OPENAI_API_KEY", self.config.get("api_key"))
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        # Default LLM config
        return {
            "model": self.config.get("model", "gpt-4"),
            "temperature": self.config.get("temperature", 0.7),
            "api_key": api_key
        }
    
    def _create_autogen_agent(self) -> Any:
        """Create the underlying AutoGen agent."""
        raise NotImplementedError("Subclasses must implement _create_autogen_agent()")


# Agent registry for factory pattern
class AgentRegistry:
    """Registry for agent types."""
    
    _registry: Dict[str, Type[AgentBase]] = {}
    
    @classmethod
    def register(cls, agent_type: str) -> callable:
        """Register an agent class with the registry."""
        def decorator(agent_class: Type[AgentBase]) -> Type[AgentBase]:
            cls._registry[agent_type] = agent_class
            return agent_class
        return decorator
    
    @classmethod
    def get_agent_class(cls, agent_type: str) -> Optional[Type[AgentBase]]:
        """Get an agent class by type."""
        return cls._registry.get(agent_type)


# Agent factory
class AgentFactory:
    """Factory for creating and configuring agents."""
    
    @staticmethod
    def create_agent(agent_type: str, config: Optional[Dict[str, Any]] = None) -> AgentBase:
        """Create an agent of the specified type."""
        agent_class = AgentRegistry.get_agent_class(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_class(config or {})


# Group chat manager
class GroupChatManager:
    """Manages multi-agent conversations using AutoGen's GroupChat."""
    
    def __init__(self, agents: List[AutoGenAgentBase], config: Optional[Dict[str, Any]] = None):
        self.agents = agents
        self.config = config or {}
        self.autogen_agents = [agent.agent for agent in agents]
        self.group_chat = self._create_group_chat()
    
    def _create_group_chat(self) -> Any:
        """Create an AutoGen GroupChat instance."""
        return autogen.GroupChat(
            agents=self.autogen_agents,
            messages=[],
            max_round=self.config.get("max_round", 10)
        )
    
    def start_chat(self, message: str) -> Dict[str, Any]:
        """Start a group chat with the given message."""
        manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=self.config.get("llm_config", {})
        )
        
        # Start the chat with the given message
        result = manager.run(message)
        return {"result": result, "messages": self.group_chat.messages}


# Example specialized agents
@AgentRegistry.register("assistant")
class AssistantAgent(AutoGenAgentBase):
    """Assistant agent that can answer questions and perform tasks."""
    
    def _create_autogen_agent(self) -> Any:
        """Create an AutoGen AssistantAgent."""
        return autogen.AssistantAgent(
            name=self.config.get("name", "Assistant"),
            system_message=self.config.get("system_message", "You are a helpful assistant."),
            llm_config=self.llm_config
        )
    
    def run(self, message: str) -> str:
        """Run the assistant agent with a message."""
        response = self.agent.generate_reply(
            messages=[{"role": "user", "content": message}],
            sender={"name": "User"}
        )
        return response


@AgentRegistry.register("user_proxy")
class UserProxyAgent(AutoGenAgentBase):
    """User proxy agent that represents a human user."""
    
    def _create_autogen_agent(self) -> Any:
        """Create an AutoGen UserProxyAgent."""
        return autogen.UserProxyAgent(
            name=self.config.get("name", "User"),
            human_input_mode=self.config.get("human_input_mode", "NEVER"),
            max_consecutive_auto_reply=self.config.get("max_consecutive_auto_reply", 5),
            code_execution_config=self.config.get("code_execution_config", {"work_dir": "workspace"})
        )
    
    def run(self, message: str) -> str:
        """Run the user proxy agent with a message."""
        response = self.agent.generate_reply(
            messages=[{"role": "assistant", "content": message}],
            sender={"name": "Assistant"}
        )
        return response


@AgentRegistry.register("code_executor")
class CodeExecutorAgent(AutoGenAgentBase):
    """Agent that executes code in a safe environment."""
    
    def _create_autogen_agent(self) -> Any:
        """Create an AutoGen UserProxyAgent configured for code execution."""
        return autogen.UserProxyAgent(
            name=self.config.get("name", "CodeExecutor"),
            human_input_mode="NEVER",
            system_message="I am a code execution agent. I can run code and return the results.",
            code_execution_config={
                "work_dir": self.config.get("work_dir", "workspace"),
                "use_docker": self.config.get("use_docker", False),
                "timeout": self.config.get("timeout", 60)
            }
        )
    
    def run(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Run code and return the results."""
        message = f"```{language}\n{code}\n```"
        response = self.agent.generate_reply(
            messages=[{"role": "assistant", "content": message}],
            sender={"name": "Assistant"}
        )
        return {"output": response, "success": "Error" not in response}


def main():
    """Run a simple example of agent collaboration."""
    # Load configuration
    try:
        config_manager = ConfigManager()
        config = config_manager.get_full_config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        print("Using default configuration")
        config = {}
    
    # Create agents
    try:
        assistant = AgentFactory.create_agent("assistant", {
            "name": "Assistant",
            "system_message": "You are a helpful assistant that can answer questions about Python programming.",
            "model": "gpt-4"
        })
        
        code_executor = AgentFactory.create_agent("code_executor", {
            "name": "CodeExecutor",
            "work_dir": "workspace",
            "use_docker": False
        })
        
        user_proxy = AgentFactory.create_agent("user_proxy", {
            "name": "User",
            "human_input_mode": "NEVER"
        })
        
        # Create group chat
        group_chat_manager = GroupChatManager(
            agents=[assistant, code_executor, user_proxy],
            config={"max_round": 10}
        )
        
        # Start chat
        print("Starting group chat...")
        result = group_chat_manager.start_chat(
            "Write a Python function to calculate the Fibonacci sequence and show me the first 10 numbers."
        )
        
        # Print results
        print("\nChat completed!")
        print("Final message:")
        if result["messages"]:
            print(result["messages"][-1]["content"])
        
    except Exception as e:
        print(f"Error running example: {e}")


if __name__ == "__main__":
    main()
