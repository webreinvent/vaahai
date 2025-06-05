"""
VaahAI Specialized Agent Base Implementation

This module provides the base class for specialized agents that perform specific tasks.
"""

import logging
from typing import Dict, Any, List, Optional

from ..conversational import ConversationalAgent

logger = logging.getLogger(__name__)


class SpecializedAgent(ConversationalAgent):
    """
    Base class for specialized agents that perform specific tasks.
    
    SpecializedAgent extends ConversationalAgent with additional functionality
    for task-specific agents, such as domain-specific knowledge and capabilities.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new specialized agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name)
        self._domain: str = ""
        self._expertise: List[str] = []
        
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        
        Raises:
            AgentConfigurationError: If the configuration is invalid
        """
        from ...exceptions import AgentConfigurationError
        
        # First validate using parent class validation
        try:
            if not super()._validate_config():
                return False
        except Exception as e:
            # Re-raise with more context
            raise AgentConfigurationError(self._name, "base_config", str(e))
        
        # Additional validation for specialized agent fields
        if 'domain' in self._config:
            if not isinstance(self._config['domain'], str):
                error_msg = "domain must be a string"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "domain", error_msg)
            self._domain = self._config['domain']
        
        # Validate expertise if provided
        if 'expertise' in self._config:
            if not isinstance(self._config['expertise'], list):
                error_msg = "expertise must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "expertise", error_msg)
            self._expertise = self._config['expertise']
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add specialized agent capabilities
        self.add_capability('domain_expertise')
        
        # Add expertise-specific capabilities
        for expertise in self._expertise:
            self.add_capability(f"expertise_{expertise}")
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response to the given message.
        
        This implementation adds domain-specific knowledge and expertise
        to the response generation process.
        
        Args:
            message: The message to respond to
            
        Returns:
            The agent's response message
        """
        # In a real implementation, this would use domain-specific knowledge
        # For now, we return a placeholder response
        return {
            'type': 'text',
            'content': f"Specialized agent {self._name} with domain '{self._domain}' is processing your request.",
            'sender': self._name,
            'recipient': message.get('sender', 'user'),
            'timestamp': self._get_timestamp()
        }
    
    def get_domain(self) -> str:
        """
        Get the domain of this specialized agent.
        
        Returns:
            Domain string
        """
        return self._domain
    
    def get_expertise(self) -> List[str]:
        """
        Get the expertise areas of this specialized agent.
        
        Returns:
            List of expertise strings
        """
        return self._expertise.copy()
