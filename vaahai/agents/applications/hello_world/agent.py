"""
Hello World agent implementation.

This module provides a simple Hello World agent that demonstrates
the basic functionality of the VaahAI agent system using the new
autogen-agentchat and autogen-ext packages.
"""

import os
import logging
import asyncio
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.messages import UserMessage, Message
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    AUTOGEN_PACKAGES_AVAILABLE = True
except ImportError:
    AUTOGEN_PACKAGES_AVAILABLE = False
    # Define dummy classes for type hints
    class AssistantAgent: pass
    class UserMessage: pass
    class Message: pass

from vaahai.agents.base.autogen_agent_base import AutoGenAgentBase
from vaahai.agents.base.agent_registry import AgentRegistry
from vaahai.agents.utils.prompt_manager import PromptManager

# Set up logging
logger = logging.getLogger(__name__)


@AgentRegistry.register("hello_world")
class HelloWorldAgent(AutoGenAgentBase):
    """
    A simple Hello World agent that demonstrates the basic functionality
    of the VaahAI agent system.
    
    This agent uses the new autogen-agentchat and autogen-ext packages
    and supports project-specific OpenAI API keys.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Hello World agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        # Call parent's init first to set up self.config
        super().__init__(config)
        
        # Set up the agent name
        self.name = self.config.get("name", "HelloWorldAgent")
        
        # Initialize the prompt manager
        self.prompt_manager = PromptManager(agent_type="hello_world", agent_name=self.name)
        
        # Load the greeting prompt
        self.greeting_prompt = self._load_greeting_prompt()
        
        # Create the agent
        if not hasattr(self, 'agent') or self.agent is None:
            self.agent = self._create_autogen_agent()
    
    def _load_greeting_prompt(self) -> str:
        """
        Load the greeting prompt from the prompt template.
        
        Returns:
            str: The greeting prompt
        """
        try:
            # Use the prompt manager to render the greeting template
            context = {
                "agent_name": self.name,
                "temperature": self.config.get("temperature", 0.7)
            }
            return self.prompt_manager.render_prompt("greeting", context)
        except Exception as e:
            logger.error(f"Error loading greeting prompt: {str(e)}")
            
            # Fallback to loading the prompt file directly if rendering fails
            try:
                module_dir = Path(__file__).parent
                prompt_path = module_dir / "prompts" / "greeting.md"
                
                with open(prompt_path, "r") as f:
                    return f.read()
            except Exception as inner_e:
                logger.error(f"Error loading greeting prompt file: {str(inner_e)}")
                
            # Ultimate fallback to a simple prompt
            return "You are a friendly AI assistant. Generate a creative greeting."
    
    def _create_autogen_agent(self) -> Any:
        """
        Create an instance of an AutoGen AssistantAgent.
        
        Returns:
            AssistantAgent: An AutoGen assistant agent instance
        """
        # If in test mode or packages not available, return a mock agent
        if self.config.get("_test_mode", False) or not AUTOGEN_PACKAGES_AVAILABLE:
            return MockAssistantAgent(name=self.name, system_message=self.greeting_prompt)
        
        # Create a model client
        model_client = self._create_model_client()
        
        # Create the assistant agent
        agent = AssistantAgent(
            name=self.name,
            system_message=self.greeting_prompt,
            llm_config=self.llm_config,
            model_client=model_client
        )
        
        return agent
    
    async def _generate_response(self, message: str = "Hello") -> str:
        """
        Generate a response using the AutoGen agent.
        
        Args:
            message: The user message to respond to, defaults to "Hello"
            
        Returns:
            str: The generated response
        """
        # If in test mode or packages not available, return a mock response
        if self.config.get("_test_mode", False) or not AUTOGEN_PACKAGES_AVAILABLE:
            return f"Hello there! This is a test response from {self.name}."
            
        # Create a user message
        user_message = UserMessage(content=message, source="user")
        
        # Get a response from the agent
        response = await self.agent.on_messages([user_message])
        
        # Extract the response content
        if response and hasattr(response, "content"):
            return response.content
        
        return "I'm sorry, I couldn't generate a greeting at this time."
    
    def run(self, message: str = "Hello") -> Dict[str, Any]:
        """
        Run the Hello World agent with the provided message.
        
        Args:
            message: The message to respond to, defaults to "Hello"
            
        Returns:
            Dict[str, Any]: A dictionary containing the response
        """
        try:
            # If in test mode or packages not available, return a mock response
            if self.config.get("_test_mode", False) or not AUTOGEN_PACKAGES_AVAILABLE:
                return {
                    "status": "success",
                    "response": f"Hello there! This is a test response from {self.name}."
                }
            
            # Run the async response generation in the event loop
            response = asyncio.run(self._generate_response(message))
            
            return {
                "status": "success",
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


class MockAssistantAgent:
    """
    A mock implementation of AssistantAgent for test mode.
    """
    
    def __init__(self, name: str, system_message: str):
        """
        Initialize the mock agent.
        
        Args:
            name: Name of the agent
            system_message: System message for the agent
        """
        self.name = name
        self.system_message = system_message
        
    async def on_messages(self, messages: List[Any]) -> Any:
        """
        Mock implementation of on_messages.
        
        Args:
            messages: List of messages
            
        Returns:
            A mock response
        """
        # Extract the last message content
        message_content = messages[-1].content if messages else "Hello"
        
        # Create a mock response object
        class MockResponse:
            def __init__(self, content):
                self.content = content
                
        return MockResponse(f"Hello there! This is a test response from {self.name}.")
