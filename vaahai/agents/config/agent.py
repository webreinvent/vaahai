"""
Agent Configuration Classes

This module provides configuration classes for agents, including basic agent
configuration and Autogen-specific agent configuration.
"""

from typing import Dict, Any, List, Optional, Union, Set

from .base import BaseConfig
from ..schemas import AUTOGEN_AGENT_CONFIG_SCHEMA


class AgentConfig(BaseConfig):
    """
    Configuration for agents.
    
    This class provides structured configuration for agents, with validation
    to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new agent configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"name", "type"}
        self._optional_fields = {
            "id": None,
            "description": "",
            "capabilities": [],
            "llm": {},
            "tools": [],
            "decorators": [],
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
        if field == "name":
            return isinstance(value, str) and len(value) > 0
        elif field == "type":
            return isinstance(value, str) and len(value) > 0
        elif field == "id":
            return value is None or (isinstance(value, str) and len(value) > 0)
        elif field == "description":
            return isinstance(value, str)
        elif field == "capabilities":
            return isinstance(value, list) and all(isinstance(c, str) for c in value)
        elif field == "llm":
            return isinstance(value, dict)
        elif field == "tools":
            return isinstance(value, list) and all(isinstance(t, dict) for t in value)
        elif field == "decorators":
            return isinstance(value, list) and all(isinstance(d, dict) for d in value)
        elif field == "metadata":
            return isinstance(value, dict)
        return True


class AutogenAgentConfig(BaseConfig):
    """
    Configuration for Autogen agents.
    
    This class provides structured configuration for Autogen agents, with validation
    using JSON schema to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new Autogen agent configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"name", "system_message"}
        self._optional_fields = {
            "human_input_mode": "NEVER",
            "max_consecutive_auto_reply": 10,
            "llm_config": None,
            "code_execution_config": None,
            "is_termination_msg": None,
            "function_map": None
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
        
        # Set schema
        self._schema = AUTOGEN_AGENT_CONFIG_SCHEMA
    
    def _validate_field(self, field: str, value: Any) -> bool:
        """
        Validate a configuration field.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if the field is valid, False otherwise
        """
        if field == "name":
            return isinstance(value, str) and len(value) > 0
        elif field == "system_message":
            return isinstance(value, str) and len(value) > 0
        elif field == "human_input_mode":
            return isinstance(value, str) and value in ["NEVER", "TERMINATE", "ALWAYS"]
        elif field == "max_consecutive_auto_reply":
            return isinstance(value, int) and value >= 0
        elif field == "llm_config":
            return value is None or isinstance(value, dict)
        elif field == "code_execution_config":
            return value is None or isinstance(value, dict)
        elif field == "is_termination_msg":
            return value is None or callable(value)
        elif field == "function_map":
            return value is None or isinstance(value, dict)
        return True
    
    def validate(self) -> bool:
        """
        Validate the Autogen agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check required fields
        for field in self._required_fields:
            if field not in self._config:
                return False
        
        # Validate each field
        for field, value in self._config.items():
            if not self._validate_field(field, value):
                return False
        
        return True
