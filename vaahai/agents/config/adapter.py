"""
Adapter Configuration Classes

This module provides configuration classes for adapters, which are used to integrate
VaahAI with external frameworks like Autogen.
"""

from typing import Dict, Any, List, Optional, Union, Set

from .base import BaseConfig


class AdapterConfig(BaseConfig):
    """
    Configuration for adapters.
    
    This class provides structured configuration for adapters, with validation
    to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new adapter configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"framework"}
        self._optional_fields = {
            "agent_type": "assistant",
            "chat_type": "round_robin",
            "agent_config": {},
            "chat_config": {},
            "metadata": {}
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
    
    def _validate_field(self, field: str, value: Any) -> bool:
        """
        Validate a configuration field.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if the field is valid, False otherwise
        """
        if field == "framework":
            return isinstance(value, str) and value in ["autogen", "langchain", "custom"]
        elif field == "agent_type":
            return isinstance(value, str) and value in ["assistant", "user_proxy", "conversational"]
        elif field == "chat_type":
            return isinstance(value, str) and value in ["round_robin", "selector", "broadcast"]
        elif field == "agent_config":
            return isinstance(value, dict)
        elif field == "chat_config":
            return isinstance(value, dict)
        elif field == "metadata":
            return isinstance(value, dict)
        return True
