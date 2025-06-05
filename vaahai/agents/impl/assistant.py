"""
VaahAI Assistant Agent Implementation

This module provides the AssistantAgent class, which implements an AI assistant
that can respond to user queries and perform tasks.
"""

import logging
from typing import Dict, Any, List, Optional

from ..base import BaseAgent
from .conversational import ConversationalAgent

logger = logging.getLogger(__name__)


class AssistantAgent(ConversationalAgent):
    """
    An agent implementation for AI assistants.
    
    AssistantAgent extends ConversationalAgent with additional capabilities
    specific to AI assistants, such as tool usage, personalization,
    and more advanced response generation.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new assistant agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name)
        self._tools: Dict[str, Any] = {}
        self._system_prompt: str = ""
        
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # First validate using parent class validation
        if not super()._validate_config():
            return False
        
        # Additional validation for assistant-specific fields
        if 'system_prompt' in self._config:
            if not isinstance(self._config['system_prompt'], str):
                logger.error("system_prompt must be a string")
                return False
            self._system_prompt = self._config['system_prompt']
        
        # Validate tools if provided
        if 'tools' in self._config:
            if not isinstance(self._config['tools'], list):
                logger.error("tools must be a list")
                return False
            
            for tool in self._config['tools']:
                if not isinstance(tool, dict) or 'name' not in tool:
                    logger.error("Each tool must be a dictionary with at least a 'name' field")
                    return False
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add assistant-specific capabilities
        self.add_capability('personalized_responses')
        
        # Add tool capabilities if tools are configured
        if 'tools' in self._config and isinstance(self._config['tools'], list):
            self.add_capability('tool_use')
            
            # Register tools
            for tool_config in self._config['tools']:
                self._register_tool(tool_config)
    
    def _register_tool(self, tool_config: Dict[str, Any]) -> None:
        """
        Register a tool with this assistant.
        
        Args:
            tool_config: Tool configuration dictionary
        """
        tool_name = tool_config['name']
        logger.info(f"Registering tool '{tool_name}' with assistant {self._name}")
        
        # In a real implementation, this would create or load the actual tool
        # For now, we just store the tool configuration
        self._tools[tool_name] = tool_config
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response to the given message.
        
        This implementation adds assistant-specific functionality such as
        tool usage and personalization.
        
        Args:
            message: The message to respond to
            
        Returns:
            The agent's response message
        """
        # In a real implementation, this would use an LLM to generate a response
        # For now, we return a placeholder response
        content = f"Assistant {self._name} is processing your request."
        
        # Check if the message contains a tool request
        if 'tool' in message:
            tool_name = message['tool']
            if tool_name in self._tools:
                content = f"Assistant {self._name} is using the {tool_name} tool to process your request."
        
        return {
            'type': 'text',
            'content': content,
            'sender': self._name,
            'recipient': message.get('sender', 'user'),
            'timestamp': self._get_timestamp()
        }
    
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this assistant.
        
        Returns:
            The system prompt string
        """
        return self._system_prompt
    
    def set_system_prompt(self, prompt: str) -> None:
        """
        Set the system prompt for this assistant.
        
        Args:
            prompt: The new system prompt
        """
        self._system_prompt = prompt
        
    def get_available_tools(self) -> List[str]:
        """
        Get the names of all tools available to this assistant.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())
