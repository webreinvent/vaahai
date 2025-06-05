"""
VaahAI Conversational Agent Implementation

This module provides the ConversationalAgent class, which is a base implementation
for agents that engage in conversation with users or other agents.
"""

import logging
from typing import Dict, Any, List, Optional

from ..base import BaseAgent
from ..config.agent import AgentConfig

logger = logging.getLogger(__name__)


class ConversationalAgent(BaseAgent):
    """
    A base agent implementation for conversational agents.
    
    ConversationalAgent provides core functionality for agents that engage
    in conversation, including message handling, response generation,
    and conversation history management.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new conversational agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name)
        self._conversation_history: List[Dict[str, Any]] = []
        self._max_history_length = 100  # Default value, can be overridden in config
        
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        required_fields = ['name', 'type']
        
        for field in required_fields:
            if field not in self._config:
                logger.error(f"Missing required field '{field}' in agent configuration")
                return False
        
        # Validate max_history_length if provided
        if 'max_history_length' in self._config:
            try:
                self._max_history_length = int(self._config['max_history_length'])
                if self._max_history_length <= 0:
                    logger.error("max_history_length must be a positive integer")
                    return False
            except (ValueError, TypeError):
                logger.error("max_history_length must be a positive integer")
                return False
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Add basic conversational capabilities
        self.add_capability('text_response')
        self.add_capability('conversation_history')
        
        # Add additional capabilities from config if specified
        if 'capabilities' in self._config and isinstance(self._config['capabilities'], list):
            for capability in self._config['capabilities']:
                self.add_capability(capability)
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and return a response.
        
        Args:
            message: The message to process
            
        Returns:
            The agent's response message
            
        Raises:
            ValueError: If the agent is not initialized
        """
        if not self._initialized:
            raise ValueError(f"Agent {self._name} is not initialized")
        
        # Add message to conversation history
        self._add_to_history(message)
        
        # Generate response (to be implemented by subclasses)
        response = await self._generate_response(message)
        
        # Add response to conversation history
        self._add_to_history(response)
        
        return response
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response to the given message.
        
        This method should be overridden by subclasses to implement
        specific response generation logic.
        
        Args:
            message: The message to respond to
            
        Returns:
            The agent's response message
        """
        # Default implementation returns a simple acknowledgment
        return {
            'type': 'text',
            'content': f"Agent {self._name} received your message.",
            'sender': self._name,
            'recipient': message.get('sender', 'user'),
            'timestamp': self._get_timestamp()
        }
    
    def _add_to_history(self, message: Dict[str, Any]) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            message: The message to add
        """
        self._conversation_history.append(message)
        
        # Trim history if it exceeds the maximum length
        if len(self._conversation_history) > self._max_history_length:
            self._conversation_history = self._conversation_history[-self._max_history_length:]
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.
        
        Returns:
            List of messages in the conversation history
        """
        return self._conversation_history.copy()
    
    def clear_conversation_history(self) -> None:
        """
        Clear the conversation history.
        """
        self._conversation_history = []
    
    def _get_timestamp(self) -> str:
        """
        Get the current timestamp as an ISO 8601 string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.utcnow().isoformat()
