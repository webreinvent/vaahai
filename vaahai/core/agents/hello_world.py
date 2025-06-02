"""
Hello World Agent

A simple agent implementation to validate the Autogen integration framework.
"""

from typing import Dict, Any, Optional
from .base import VaahaiAgent


class HelloWorldAgent(VaahaiAgent):
    """Simple Hello World agent for testing the Autogen integration."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Hello World agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        super().__init__(config)
        self.message = self.config.get("message", "Hello, World!")
        
    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Run the Hello World agent.
        
        Returns:
            A dictionary containing the success status, message, and agent type
        """
        return {
            "success": True,
            "message": self.message,
            "agent_type": "hello_world"
        }
