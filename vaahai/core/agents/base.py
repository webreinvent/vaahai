"""
Base Agent Class

This module defines the base class for all Vaahai agents.
"""

from typing import Dict, Any, Optional


class VaahaiAgent:
    """Base class for all Vaahai agents."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent with configuration.
        
        Args:
            config: Configuration dictionary for the agent
        """
        self.config = config or {}
        
    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Run the agent with the given arguments.
        
        Returns:
            A dictionary containing the results of the agent execution
        
        Raises:
            NotImplementedError: If the subclass does not implement this method
        """
        raise NotImplementedError("Subclasses must implement run method")
