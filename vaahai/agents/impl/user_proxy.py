"""
VaahAI User Proxy Agent Implementation

This module provides the UserProxyAgent class, which represents a user
in the agent system, allowing for human-in-the-loop interactions.
"""

import logging
from typing import Dict, Any, List, Optional, Callable, Awaitable

from ..base import BaseAgent
from .conversational import ConversationalAgent

logger = logging.getLogger(__name__)


class UserProxyAgent(ConversationalAgent):
    """
    An agent implementation that represents a user in the system.
    
    UserProxyAgent extends ConversationalAgent to provide a bridge between
    the agent system and a human user, enabling human-in-the-loop interactions.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new user proxy agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name)
        self._human_input_mode = "ALWAYS"  # Default to always ask for human input
        self._input_callback: Optional[Callable[[str], Awaitable[str]]] = None
        self._max_consecutive_auto_reply = 0
        self._consecutive_auto_reply_counter = 0
        
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # First validate using parent class validation
        if not super()._validate_config():
            return False
        
        # Additional validation for user proxy specific fields
        if 'human_input_mode' in self._config:
            mode = self._config['human_input_mode']
            valid_modes = ["ALWAYS", "NEVER", "TERMINATE", "AUTO"]
            if mode not in valid_modes:
                logger.error(f"Invalid human_input_mode '{mode}'. Must be one of {valid_modes}")
                return False
            self._human_input_mode = mode
        
        # Validate max_consecutive_auto_reply if provided
        if 'max_consecutive_auto_reply' in self._config:
            try:
                self._max_consecutive_auto_reply = int(self._config['max_consecutive_auto_reply'])
                if self._max_consecutive_auto_reply < 0:
                    logger.error("max_consecutive_auto_reply must be a non-negative integer")
                    return False
            except (ValueError, TypeError):
                logger.error("max_consecutive_auto_reply must be a non-negative integer")
                return False
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add user proxy specific capabilities
        self.add_capability('human_input')
        
        # Add auto-reply capability if configured
        if self._human_input_mode in ["AUTO", "NEVER"]:
            self.add_capability('auto_reply')
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and return a response.
        
        For UserProxyAgent, this typically involves getting input from the human user.
        
        Args:
            message: The message to process
            
        Returns:
            The user's response message
            
        Raises:
            ValueError: If the agent is not initialized or no input callback is set
        """
        if not self._initialized:
            raise ValueError(f"Agent {self._name} is not initialized")
        
        if self._input_callback is None:
            raise ValueError(f"No input callback set for UserProxyAgent {self._name}")
        
        # Add message to conversation history
        self._add_to_history(message)
        
        # Determine if we should get human input or auto-reply
        should_get_human_input = self._should_get_human_input(message)
        
        # Generate response
        if should_get_human_input:
            response = await self._get_human_input(message)
            self._consecutive_auto_reply_counter = 0
        else:
            response = await self._generate_auto_reply(message)
            self._consecutive_auto_reply_counter += 1
        
        # Add response to conversation history
        self._add_to_history(response)
        
        return response
    
    def _should_get_human_input(self, message: Dict[str, Any]) -> bool:
        """
        Determine if human input should be requested for this message.
        
        Args:
            message: The message to process
            
        Returns:
            True if human input should be requested, False otherwise
        """
        if self._human_input_mode == "ALWAYS":
            return True
        elif self._human_input_mode == "NEVER":
            return False
        elif self._human_input_mode == "TERMINATE":
            # Check if message contains a termination signal
            content = message.get('content', '').lower()
            terminate_signals = ["terminate", "exit", "quit", "end", "stop"]
            return any(signal in content for signal in terminate_signals)
        elif self._human_input_mode == "AUTO":
            # Auto mode: get human input if max consecutive auto replies reached
            return self._consecutive_auto_reply_counter >= self._max_consecutive_auto_reply
        
        # Default to getting human input
        return True
    
    async def _get_human_input(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get input from the human user.
        
        Args:
            message: The message to respond to
            
        Returns:
            The user's response message
        """
        # Format the message for display to the user
        display_message = self._format_message_for_display(message)
        
        # Get input from the user via the callback
        user_input = await self._input_callback(display_message)
        
        # Format the user's input as a response message
        return {
            'type': 'text',
            'content': user_input,
            'sender': self._name,
            'recipient': message.get('sender', 'assistant'),
            'timestamp': self._get_timestamp()
        }
    
    async def _generate_auto_reply(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an automatic reply when human input is not required.
        
        Args:
            message: The message to respond to
            
        Returns:
            The auto-generated response message
        """
        # In a real implementation, this would use an LLM or rule-based system
        # For now, we return a simple acknowledgment
        return {
            'type': 'text',
            'content': f"Auto-reply from {self._name}: Acknowledged.",
            'sender': self._name,
            'recipient': message.get('sender', 'assistant'),
            'timestamp': self._get_timestamp(),
            'is_auto_reply': True
        }
    
    def _format_message_for_display(self, message: Dict[str, Any]) -> str:
        """
        Format a message for display to the human user.
        
        Args:
            message: The message to format
            
        Returns:
            Formatted message string
        """
        sender = message.get('sender', 'Unknown')
        content = message.get('content', '')
        return f"{sender}: {content}"
    
    def set_input_callback(self, callback: Callable[[str], Awaitable[str]]) -> None:
        """
        Set the callback function for getting human input.
        
        Args:
            callback: A function that takes a prompt string and returns a future
                     that resolves to the user's input string
        """
        self._input_callback = callback
    
    def get_human_input_mode(self) -> str:
        """
        Get the current human input mode.
        
        Returns:
            The human input mode string
        """
        return self._human_input_mode
    
    def set_human_input_mode(self, mode: str) -> None:
        """
        Set the human input mode.
        
        Args:
            mode: The new human input mode. Must be one of "ALWAYS", "NEVER", "TERMINATE", or "AUTO".
            
        Raises:
            ValueError: If the mode is invalid
        """
        valid_modes = ["ALWAYS", "NEVER", "TERMINATE", "AUTO"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid human_input_mode '{mode}'. Must be one of {valid_modes}")
        
        self._human_input_mode = mode
