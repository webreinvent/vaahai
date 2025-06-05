"""
LLM Configuration Classes

This module provides configuration classes for LLMs (Large Language Models),
with validation to ensure that required fields are present and have valid values.
"""

from typing import Dict, Any, List, Optional, Union, Set

from .base import BaseConfig
from ..schemas import CONFIG_LIST_SCHEMA


class LLMConfig(BaseConfig):
    """
    Configuration for LLMs.
    
    This class provides structured configuration for LLMs, with validation
    using JSON schema to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new LLM configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"model"}
        self._optional_fields = {
            "api_key": None,
            "api_type": "openai",
            "api_rate_limit": None,
            "base_url": None,
            "api_version": None,
            "organization": None,
            "tags": [],
            "metadata": {}
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
    
    def validate(self) -> bool:
        """
        Validate the configuration based on the API type.
        
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
        
        # Additional validation based on API type
        api_type = self._config.get("api_type", "openai")
        
        if api_type == "openai":
            # OpenAI requires either an API key or Azure configuration
            if not self._config.get("api_key") and not (
                self._config.get("base_url") and 
                self._config.get("api_version")
            ):
                return False
        elif api_type == "azure":
            # Azure requires base_url and api_version
            if not self._config.get("base_url") or not self._config.get("api_version"):
                return False
        
        return True
    
    def _validate_field(self, field: str, value: Any) -> bool:
        """
        Validate a configuration field.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if the field is valid, False otherwise
        """
        if field == "model":
            return isinstance(value, str) and len(value) > 0
        elif field == "api_key":
            return value is None or (isinstance(value, str) and len(value) > 0)
        elif field == "api_type":
            return isinstance(value, str) and value in ["openai", "azure", "anthropic", "cohere", "huggingface", "custom"]
        elif field == "api_rate_limit":
            return value is None or isinstance(value, (int, float)) and value > 0
        elif field == "base_url":
            return value is None or (isinstance(value, str) and len(value) > 0)
        elif field == "api_version":
            return value is None or (isinstance(value, str) and len(value) > 0)
        elif field == "organization":
            return value is None or (isinstance(value, str) and len(value) > 0)
        elif field == "tags":
            return isinstance(value, list) and all(isinstance(tag, str) for tag in value)
        elif field == "metadata":
            return isinstance(value, dict)
        return True
