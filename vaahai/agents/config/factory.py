"""
Configuration Factory

This module provides a factory for creating configuration objects from dictionaries,
JSON strings, and files. It supports all configuration types defined in this package.
"""

import json
from typing import Dict, Any, List, Optional, Union, Set, Type

from .base import BaseConfig
from .agent import AgentConfig, AutogenAgentConfig
from .group_chat import GroupChatConfig, AutogenGroupChatConfig
from .tool import ToolConfig, AutogenToolConfig
from .adapter import AdapterConfig
from .llm import LLMConfig


class ConfigFactory:
    """
    Factory for creating configuration objects.
    
    This class provides methods for creating configuration objects from dictionaries,
    JSON strings, and files. It supports all configuration types defined in this module.
    """
    
    _config_types = {
        'agent': AgentConfig,
        'group_chat': GroupChatConfig,
        'tool': ToolConfig,
        'adapter': AdapterConfig,
        'autogen_agent': AutogenAgentConfig,
        'autogen_group_chat': AutogenGroupChatConfig,
        'autogen_tool': AutogenToolConfig,
        'llm': LLMConfig
    }
    
    @classmethod
    def from_dict(cls, config_type: str, config_dict: Dict[str, Any]) -> BaseConfig:
        """
        Create a configuration object from a dictionary.
        
        Args:
            config_type: Type of configuration to create
            config_dict: Dictionary containing configuration parameters
            
        Returns:
            Configuration object
            
        Raises:
            ValueError: If the configuration type is not supported
        """
        config_class = cls.get_config_class(config_type)
        return config_class(**config_dict)
    
    @classmethod
    def from_json(cls, config_type: str, json_string: str) -> BaseConfig:
        """
        Create a configuration object from a JSON string.
        
        Args:
            config_type: Type of configuration to create
            json_string: JSON string containing configuration parameters
            
        Returns:
            Configuration object
            
        Raises:
            ValueError: If the configuration type is not supported
            json.JSONDecodeError: If the JSON string is invalid
        """
        config_dict = json.loads(json_string)
        return cls.from_dict(config_type, config_dict)
    
    @classmethod
    def from_file(cls, config_type: str, file_path: str) -> BaseConfig:
        """
        Create a configuration object from a file.
        
        Args:
            config_type: Type of configuration to create
            file_path: Path to the configuration file
            
        Returns:
            Configuration object
            
        Raises:
            ValueError: If the configuration type is not supported
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_type, config_dict)
    
    @classmethod
    def get_config_class(cls, config_type: str) -> Type[BaseConfig]:
        """
        Get the configuration class for a given type.
        
        Args:
            config_type: Type of configuration
            
        Returns:
            Configuration class
            
        Raises:
            ValueError: If the configuration type is not supported
        """
        if config_type not in cls._config_types:
            raise ValueError(f"Unsupported configuration type: {config_type}")
        return cls._config_types[config_type]
    
    @classmethod
    def register_config_type(cls, config_type: str, config_class: Type[BaseConfig]) -> None:
        """
        Register a new configuration type.
        
        Args:
            config_type: Type of configuration
            config_class: Configuration class
        """
        cls._config_types[config_type] = config_class
