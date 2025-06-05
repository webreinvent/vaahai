"""
Base Configuration Classes

This module provides the base configuration classes and interfaces used by all
configuration types in the VaahAI system.
"""

from abc import abstractmethod
import json
import jsonschema
from typing import Dict, Any, List, Optional, Union, Set, Type

from ..interfaces import IConfig


class BaseConfig(IConfig):
    """
    Base class for all configuration objects.
    
    This class provides common functionality for configuration objects,
    such as validation and conversion to dictionary.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new configuration object.
        
        Args:
            **kwargs: Configuration parameters
        """
        self._config = kwargs
        self._required_fields: Set[str] = set()
        self._optional_fields: Dict[str, Any] = {}
        self._schema: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        return self._config
    
    def to_json(self) -> str:
        """
        Convert configuration to JSON string.
        
        Returns:
            JSON string representation of the configuration
        """
        return json.dumps(self._config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value to return if key is not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        
    def validate(self) -> bool:
        """
        Validate the configuration.
        
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
        
        # Validate against schema if available
        if self._schema:
            try:
                jsonschema.validate(instance=self._config, schema=self._schema)
            except jsonschema.exceptions.ValidationError:
                return False
        
        return True
    
    @abstractmethod
    def _validate_field(self, field: str, value: Any) -> bool:
        """
        Validate a configuration field.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if the field is valid, False otherwise
        """
        pass
