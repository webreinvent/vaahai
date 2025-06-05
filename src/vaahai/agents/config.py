"""
VaahAI Agent Configuration

This module provides configuration classes for agents, group chats, and related components.
These classes implement the IConfig interface and provide structured configuration
with validation, enhancing reusability and extensibility by separating configuration
from implementation.
"""

from abc import abstractmethod
from typing import Dict, Any, List, Optional, Union, Set, Type

from .interfaces import IConfig


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
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        return self._config.copy()
    
    def validate(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
        """
        # Check that all required fields are present
        for field in self._required_fields:
            if field not in self._config:
                return False
        
        # Check that all fields have valid types
        for field, value in self._config.items():
            if not self._validate_field(field, value):
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
        # By default, all fields are valid
        return True
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value to return if the key is not found
            
        Returns:
            Configuration value, or default if not found
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
    
    def update(self, config: Dict[str, Any]) -> None:
        """
        Update configuration with values from a dictionary.
        
        Args:
            config: Dictionary containing configuration values
        """
        self._config.update(config)


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
        if field == "name" and not isinstance(value, str):
            return False
        elif field == "type" and not isinstance(value, str):
            return False
        elif field == "id" and value is not None and not isinstance(value, str):
            return False
        elif field == "description" and not isinstance(value, str):
            return False
        elif field == "capabilities" and not isinstance(value, list):
            return False
        elif field == "llm" and not isinstance(value, dict):
            return False
        elif field == "tools" and not isinstance(value, list):
            return False
        elif field == "decorators" and not isinstance(value, list):
            return False
        elif field == "metadata" and not isinstance(value, dict):
            return False
        
        return True


class GroupChatConfig(BaseConfig):
    """
    Configuration for group chats.
    
    This class provides structured configuration for group chats, with validation
    to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new group chat configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"type"}
        self._optional_fields = {
            "name": "GroupChat",
            "agents": [],
            "max_rounds": 10,
            "termination_conditions": [],
            "selector": None,
            "human_input_mode": "NEVER",
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
        if field == "type" and not isinstance(value, str):
            return False
        elif field == "name" and not isinstance(value, str):
            return False
        elif field == "agents" and not isinstance(value, list):
            return False
        elif field == "max_rounds" and not isinstance(value, int):
            return False
        elif field == "termination_conditions" and not isinstance(value, list):
            return False
        elif field == "selector" and value is not None and not isinstance(value, dict):
            return False
        elif field == "human_input_mode" and not isinstance(value, str):
            return False
        elif field == "metadata" and not isinstance(value, dict):
            return False
        
        return True


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
        if field == "name" and not isinstance(value, str):
            return False
        elif field == "type" and not isinstance(value, str):
            return False
        elif field == "description" and not isinstance(value, str):
            return False
        elif field == "parameters" and not isinstance(value, dict):
            return False
        elif field == "metadata" and not isinstance(value, dict):
            return False
        
        return True


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
        if field == "framework" and not isinstance(value, str):
            return False
        elif field == "agent_type" and not isinstance(value, str):
            return False
        elif field == "chat_type" and not isinstance(value, str):
            return False
        elif field == "agent_config" and not isinstance(value, dict):
            return False
        elif field == "chat_config" and not isinstance(value, dict):
            return False
        elif field == "metadata" and not isinstance(value, dict):
            return False
        
        return True


class ConfigFactory:
    """
    Factory for creating configuration objects.
    
    This factory provides methods for creating different types of configuration objects,
    centralizing configuration creation logic and enhancing extensibility.
    """
    
    _config_classes: Dict[str, Type[BaseConfig]] = {
        "agent": AgentConfig,
        "group_chat": GroupChatConfig,
        "tool": ToolConfig,
        "adapter": AdapterConfig
    }
    
    @classmethod
    def create_config(cls, config_type: str, **kwargs) -> BaseConfig:
        """
        Create a configuration object of the specified type.
        
        Args:
            config_type: Type of configuration to create
            **kwargs: Configuration parameters
            
        Returns:
            Configuration object
            
        Raises:
            ValueError: If the configuration type is not supported
        """
        if config_type not in cls._config_classes:
            raise ValueError(f"Unsupported configuration type: {config_type}")
        
        config_class = cls._config_classes[config_type]
        return config_class(**kwargs)
    
    @classmethod
    def register_config_class(cls, config_type: str, config_class: Type[BaseConfig]) -> None:
        """
        Register a configuration class.
        
        Args:
            config_type: Type of configuration
            config_class: Configuration class to register
        """
        cls._config_classes[config_type] = config_class
    
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
        return cls.create_config(config_type, **config_dict)
    
    @classmethod
    def get_supported_config_types(cls) -> List[str]:
        """
        Get a list of supported configuration types.
        
        Returns:
            List of configuration type names
        """
        return list(cls._config_classes.keys())
