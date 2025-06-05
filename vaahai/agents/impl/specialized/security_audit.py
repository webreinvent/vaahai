"""
VaahAI Security Audit Agent Implementation

This module provides the SecurityAuditAgent class, which specializes in
security vulnerability detection and compliance checking.
"""

import logging
from typing import Dict, Any, List, Optional

from ...exceptions import AgentConfigurationError, AgentCommunicationError, SecurityAuditError, AgentMessageError
from .base import SpecializedAgent

logger = logging.getLogger(__name__)


class SecurityAuditAgent(SpecializedAgent):
    """
    A specialized agent for security auditing.
    
    SecurityAuditAgent extends SpecializedAgent with capabilities specific to
    security auditing, such as vulnerability detection, compliance checking,
    and security best practices.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new security audit agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name or "SecurityAuditor")
        self._compliance_standards: List[str] = []
        self._vulnerability_categories: List[str] = []
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the agent with the provided configuration.
        
        Args:
            config: Configuration dictionary for the agent
            
        Returns:
            True if initialization was successful, False otherwise
        """
        # Update the agent name if provided in the config
        if 'name' in config and isinstance(config['name'], str):
            self._name = config['name']
        
        # Continue with normal initialization
        return super().initialize(config)
    
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
            
        Raises:
            AgentConfigurationError: If the configuration is invalid
        """
        # First validate using parent class validation
        try:
            if not super()._validate_config():
                return False
        except Exception as e:
            # Re-raise with more context
            raise AgentConfigurationError(self._name, "base_config", str(e))
        
        # Validate compliance standards if provided
        if 'compliance_standards' in self._config:
            if not isinstance(self._config['compliance_standards'], list):
                error_msg = "compliance_standards must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "compliance_standards", error_msg)
            
            for standard in self._config['compliance_standards']:
                if not isinstance(standard, str):
                    error_msg = "each compliance standard must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "compliance_standards", error_msg)
            
            self._compliance_standards = self._config['compliance_standards']
        else:
            logger.warning(f"No compliance standards specified for {self._name}, using empty list")
            self._compliance_standards = []
        
        # Validate vulnerability categories if provided
        if 'vulnerability_categories' in self._config:
            if not isinstance(self._config['vulnerability_categories'], list):
                error_msg = "vulnerability_categories must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "vulnerability_categories", error_msg)
            
            for category in self._config['vulnerability_categories']:
                if not isinstance(category, str):
                    error_msg = "each vulnerability category must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "vulnerability_categories", error_msg)
            
            self._vulnerability_categories = self._config['vulnerability_categories']
        else:
            logger.info(f"No vulnerability categories specified for {self._name}, using default categories")
            self._vulnerability_categories = ["injection", "authentication", "authorization", "data_exposure"]
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add security audit capabilities
        self.add_capability('security_audit')
        self.add_capability('vulnerability_detection')
        
        # Add compliance-specific capabilities
        for standard in self._compliance_standards:
            self.add_capability(f"compliance_{standard}")
        
        # Add vulnerability-specific capabilities
        for category in self._vulnerability_categories:
            self.add_capability(f"vulnerability_{category}")
    
    def get_compliance_standards(self) -> List[str]:
        """
        Get the list of compliance standards supported by this agent.
        
        Returns:
            List of supported compliance standard identifiers
        """
        return self._compliance_standards
    
    def get_vulnerability_categories(self) -> List[str]:
        """
        Get the list of vulnerability categories this agent can detect.
        
        Returns:
            List of vulnerability category identifiers
        """
        return self._vulnerability_categories
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a security audit response for the given message.
        
        Args:
            message: The message containing code or system to audit
            
        Returns:
            Security audit response message
            
        Raises:
            AgentMessageError: If the message format is invalid
            SecurityAuditError: If there is an error during security audit
        """
        try:
            # Validate message format
            if not isinstance(message, dict):
                raise AgentMessageError(self._name, "unknown", "Message must be a dictionary")
            
            message_type = message.get('type', 'unknown')
            
            if 'code' not in message and 'system' not in message:
                raise AgentMessageError(
                    self._name,
                    message_type,
                    "Message must contain 'code' or 'system' field for audit"
                )
            
            # In a real implementation, this would analyze the code/system and provide security findings
            # For now, we return a placeholder response
            code = message.get('code', '')
            system = message.get('system', '')
            
            target = code if code else system
            target_snippet = target[:30] + "..." if len(target) > 30 else target
            
            return {
                'type': 'security_audit',
                'content': f"Security Audit Agent {self._name} has audited your {message_type}: '{target_snippet}'",
                'sender': self._name,
                'recipient': message.get('sender', 'user'),
                'timestamp': self._get_timestamp(),
                'audit_summary': "This is a placeholder security audit.",
                'findings': [
                    {
                        'severity': 'medium',
                        'category': 'authentication',
                        'description': "Potential authentication issue detected.",
                        'recommendation': "Implement proper authentication mechanisms."
                    },
                    {
                        'severity': 'low',
                        'category': 'data_exposure',
                        'description': "Possible sensitive data exposure.",
                        'recommendation': "Encrypt sensitive data in transit and at rest."
                    }
                ],
                'compliance': {
                    standard: {'compliant': False, 'issues': 2}
                    for standard in self._compliance_standards
                }
            }
        except (AgentMessageError, SecurityAuditError) as e:
            # Re-raise specialized exceptions
            logger.error(f"Error in security audit: {str(e)}")
            raise
        except Exception as e:
            # Wrap other exceptions
            logger.error(f"Unexpected error generating security audit response: {str(e)}")
            raise SecurityAuditError(
                self._name,
                f"Failed to generate security audit: {str(e)}"
            )
