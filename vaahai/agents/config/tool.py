"""
Tool Configuration Classes

This module provides configuration classes for tools, including basic tool
configuration and Autogen-specific tool configuration.
"""

from typing import Dict, Any, List, Optional, Union, Set

from .base import BaseConfig
from ..schemas import AUTOGEN_TOOL_CONFIG_SCHEMA


class ToolConfig(BaseConfig):
    """
    Configuration for tools.
    
    This class provides structured configuration for tools, with validation
    to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new tool configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"name", "type"}
        self._optional_fields = {
            "description": "",
            "parameters": {},
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
        elif field == "description":
            return isinstance(value, str)
        elif field == "parameters":
            return isinstance(value, dict)
        elif field == "metadata":
            return isinstance(value, dict)
        return True


class AutogenToolConfig(BaseConfig):
    """
    Configuration for Autogen tools.
    
    This class provides structured configuration for Autogen tools, with validation
    using JSON schema to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new Autogen tool configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"name", "description"}
        self._optional_fields = {
            "parameters": {},
            "return_direct": False,
            "metadata": {}
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
        
        # Set schema
        self._schema = AUTOGEN_TOOL_CONFIG_SCHEMA
    
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
        elif field == "description":
            return isinstance(value, str) and len(value) > 0
        elif field == "parameters":
            return isinstance(value, dict)
        elif field == "return_direct":
            return isinstance(value, bool)
        elif field == "metadata":
            return isinstance(value, dict)
        return True
