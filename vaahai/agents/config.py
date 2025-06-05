"""
VaahAI Agent Configuration

This module provides configuration classes for agents, group chats, and related components.
These classes implement the IConfig interface and provide structured configuration
with validation, enhancing reusability and extensibility by separating configuration
from implementation.
"""

from abc import abstractmethod
import json
import jsonschema
from typing import Dict, Any, List, Optional, Union, Set, Type

from .interfaces import IConfig
from .schemas import (
    get_schema_for_config_type,
    AUTOGEN_AGENT_CONFIG_SCHEMA,
    AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA,
    AUTOGEN_TOOL_CONFIG_SCHEMA,
    CONFIG_LIST_SCHEMA
)


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
        
        # Validate each field
        for field, value in self._config.items():
            if not self._validate_field(field, value):
                return False
        
        # If schema is provided, validate against it
        if self._schema:
            try:
                jsonschema.validate(instance=self._config, schema=self._schema)
                return True
            except jsonschema.exceptions.ValidationError:
                # If schema validation fails, fall back to field validation
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
    
    def get(self, field: str, default: Any = None) -> Any:
        """
        Get a configuration field.
        
        Args:
            field: Field name
            default: Default value if field is not present
            
        Returns:
            Field value or default if field is not present
        """
        return self._config.get(field, default)
    
    def set(self, field: str, value: Any) -> None:
        """
        Set a configuration field.
        
        Args:
            field: Field name
            value: Field value
        """
        self._config[field] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration with values from a dictionary.
        
        Args:
            config_dict: Dictionary containing configuration parameters
        """
        self._config.update(config_dict)


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
            return value in ["ALWAYS", "NEVER", "TERMINATE"]
        elif field == "max_consecutive_auto_reply":
            return isinstance(value, int) and value >= 0
        elif field == "llm_config":
            # llm_config can be None or a dictionary
            return value is None or isinstance(value, dict)
        elif field == "code_execution_config":
            # code_execution_config can be None or a dictionary
            return value is None or isinstance(value, dict)
        elif field == "is_termination_msg":
            # is_termination_msg can be None or a callable or a boolean
            return value is None or callable(value) or isinstance(value, bool)
        elif field == "function_map":
            # function_map can be None or a dictionary
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


class AutogenGroupChatConfig(BaseConfig):
    """
    Configuration for Autogen group chats.
    
    This class provides structured configuration for Autogen group chats, with validation
    using JSON schema to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new Autogen group chat configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"name", "agents"}
        self._optional_fields = {
            "messages": [],
            "max_round": 10,
            "speaker_selection_method": "auto",
            "allow_repeat_speaker": False,
            "metadata": {}
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
        
        # Set schema
        self._schema = AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA
    
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
        elif field == "agents":
            return isinstance(value, list) and len(value) > 0
        elif field == "messages":
            return isinstance(value, list)
        elif field == "max_round":
            return isinstance(value, int) and value > 0
        elif field == "speaker_selection_method":
            return value in ["auto", "round_robin", "random", "manual"]
        elif field == "allow_repeat_speaker":
            return isinstance(value, bool)
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
        # Check that all required fields are present
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
            # OpenAI requires model and api_type
            return "model" in self._config and self._config["api_type"] == "openai"
        
        elif api_type == "azure":
            # Azure requires model, api_type, and base_url
            return (
                "model" in self._config and
                self._config["api_type"] == "azure" and
                "base_url" in self._config and
                self._config["base_url"] is not None
            )
        
        elif api_type == "custom":
            # Custom requires model, api_type, and base_url
            return (
                "model" in self._config and
                self._config["api_type"] == "custom" and
                "base_url" in self._config and
                self._config["base_url"] is not None
            )
        
        return False
    
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
            return value is None or isinstance(value, str)
        elif field == "api_type":
            return value in ["openai", "azure", "custom"]
        elif field == "api_rate_limit":
            return value is None or (isinstance(value, (int, float)) and value > 0)
        elif field == "base_url":
            return value is None or isinstance(value, str)
        elif field == "api_version":
            return value is None or isinstance(value, str)
        elif field == "organization":
            return value is None or isinstance(value, str)
        elif field == "tags":
            return isinstance(value, list)
        elif field == "metadata":
            return isinstance(value, dict)
        return True


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
        if config_type not in cls._config_types:
            raise ValueError(f"Unsupported configuration type: {config_type}")
        
        return cls._config_types[config_type](**config_dict)
    
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
            if file_path.endswith('.json'):
                config_dict = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        
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
