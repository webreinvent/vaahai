"""
VaahAI Configuration Loader

This module provides functionality for loading configurations from various sources,
such as files, dictionaries, and JSON strings. It also handles environment variable
substitution and validation against schemas.
"""

import os
import re
import json
import jsonschema
from typing import Dict, Any, Optional, Union, List, Type

from .config import (
    BaseConfig,
    LLMConfig,
    AutogenAgentConfig,
    AutogenGroupChatConfig,
    AutogenToolConfig,
    ConfigFactory
)


class ConfigLoadError(Exception):
    """Exception raised when a configuration cannot be loaded."""
    pass


class ConfigValidationError(Exception):
    """Exception raised when a configuration fails validation."""
    
    def __init__(self, message: str, validation_errors: List[str] = None):
        """
        Initialize a new ConfigValidationError.
        
        Args:
            message: Error message
            validation_errors: List of validation errors
        """
        self.validation_errors = validation_errors or []
        error_details = "\n- " + "\n- ".join(self.validation_errors) if self.validation_errors else ""
        super().__init__(f"{message}{error_details}")


class ConfigLoader:
    """
    Configuration loader for VaahAI.
    
    This class provides methods for loading configurations from various sources,
    such as files, dictionaries, and JSON strings. It also handles environment
    variable substitution and validation against schemas.
    """
    
    @staticmethod
    def load_from_file(file_path: str, config_type: str = None) -> Union[Dict[str, Any], BaseConfig]:
        """
        Load configuration from a file.
        
        Args:
            file_path: Path to the configuration file
            config_type: Type of configuration to load (e.g., 'llm', 'autogen_agent')
                         If None, returns the raw configuration dictionary
            
        Returns:
            Configuration dictionary or BaseConfig object
            
        Raises:
            ConfigLoadError: If the file cannot be loaded
            ConfigValidationError: If the configuration fails validation
        """
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith('.json'):
                    config_dict = json.load(f)
                else:
                    raise ConfigLoadError(f"Unsupported file format: {file_path}")
                
                # Substitute environment variables
                config_dict = ConfigLoader.substitute_env_vars(config_dict)
                
                # Return raw dictionary if no config_type is specified
                if config_type is None:
                    return config_dict
                
                # Create and validate config object
                return ConfigLoader.load_from_dict(config_dict, config_type)
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON in {file_path}: {str(e)}")
        except FileNotFoundError:
            raise ConfigLoadError(f"Configuration file not found: {file_path}")
        except Exception as e:
            if isinstance(e, (ConfigLoadError, ConfigValidationError)):
                raise
            raise ConfigLoadError(f"Error loading configuration from {file_path}: {str(e)}")
    
    @staticmethod
    def load_from_dict(config_dict: Dict[str, Any], config_type: str) -> BaseConfig:
        """
        Load configuration from a dictionary.
        
        Args:
            config_dict: Configuration dictionary
            config_type: Type of configuration to load (e.g., 'llm', 'autogen_agent')
            
        Returns:
            BaseConfig object
            
        Raises:
            ConfigValidationError: If the configuration fails validation
        """
        try:
            # Create config object
            config = ConfigFactory.from_dict(config_type, config_dict)
            
            # Validate config
            if not config.validate():
                raise ConfigValidationError(f"Invalid {config_type} configuration", 
                                          [f"Configuration failed validation for type {config_type}"])
            
            return config
        except jsonschema.exceptions.ValidationError as e:
            raise ConfigValidationError(f"Invalid {config_type} configuration", 
                                      [f"Schema validation error: {e.message}"])
        except ValueError as e:
            raise ConfigValidationError(f"Invalid {config_type} configuration", 
                                      [str(e)])
        except Exception as e:
            if isinstance(e, ConfigValidationError):
                raise
            raise ConfigLoadError(f"Error loading {config_type} configuration: {str(e)}")
    
    @staticmethod
    def load_from_json_string(json_string: str, config_type: str = None) -> Union[Dict[str, Any], BaseConfig]:
        """
        Load configuration from a JSON string.
        
        Args:
            json_string: JSON string containing configuration
            config_type: Type of configuration to load (e.g., 'llm', 'autogen_agent')
                         If None, returns the raw configuration dictionary
            
        Returns:
            Configuration dictionary or BaseConfig object
            
        Raises:
            ConfigLoadError: If the JSON string cannot be parsed
            ConfigValidationError: If the configuration fails validation
        """
        try:
            config_dict = json.loads(json_string)
            
            # Substitute environment variables
            config_dict = ConfigLoader.substitute_env_vars(config_dict)
            
            # Return raw dictionary if no config_type is specified
            if config_type is None:
                return config_dict
            
            # Create and validate config object
            return ConfigLoader.load_from_dict(config_dict, config_type)
        except json.JSONDecodeError as e:
            raise ConfigLoadError(f"Invalid JSON string: {str(e)}")
        except Exception as e:
            if isinstance(e, (ConfigLoadError, ConfigValidationError)):
                raise
            raise ConfigLoadError(f"Error loading configuration from JSON string: {str(e)}")
    
    @staticmethod
    def substitute_env_vars(config: Any) -> Any:
        """
        Substitute environment variables in a configuration.
        
        Environment variables are specified as ${VAR_NAME} and are replaced with
        their values from the environment. If the environment variable is not set,
        the placeholder is left unchanged.
        
        Args:
            config: Configuration object (can be a dictionary, list, or scalar value)
            
        Returns:
            Configuration with environment variables substituted
        """
        if isinstance(config, dict):
            return {k: ConfigLoader.substitute_env_vars(v) for k, v in config.items()}
        elif isinstance(config, list):
            return [ConfigLoader.substitute_env_vars(item) for item in config]
        elif isinstance(config, str):
            # Replace ${VAR_NAME} with environment variable value
            def replace_env_var(match):
                env_var = match.group(1)
                return os.environ.get(env_var, match.group(0))
            
            return re.sub(r'\$\{([^}]+)\}', replace_env_var, config)
        else:
            return config
    
    @staticmethod
    def load_autogen_config(file_path: str) -> Dict[str, Dict[str, BaseConfig]]:
        """
        Load a complete Autogen configuration from a file.
        
        This method loads agent, group chat, and tool configurations from a single file.
        
        Args:
            file_path: Path to the configuration file
            
        Returns:
            Dictionary containing agent, group chat, and tool configurations
            
        Raises:
            ConfigLoadError: If the file cannot be loaded
            ConfigValidationError: If any configuration fails validation
        """
        # Load raw configuration
        config_dict = ConfigLoader.load_from_file(file_path)
        
        result = {
            'agents': {},
            'group_chats': {},
            'tools': {}
        }
        
        validation_errors = []
        
        # Load agent configurations
        for agent_id, agent_config_dict in config_dict.get('agents', {}).items():
            try:
                agent_config = ConfigLoader.load_from_dict(agent_config_dict, 'autogen_agent')
                result['agents'][agent_id] = agent_config
            except ConfigValidationError as e:
                validation_errors.append(f"Agent '{agent_id}': {str(e)}")
            except Exception as e:
                validation_errors.append(f"Agent '{agent_id}': Unexpected error: {str(e)}")
        
        # Load group chat configurations
        for chat_id, chat_config_dict in config_dict.get('group_chats', {}).items():
            try:
                chat_config = ConfigLoader.load_from_dict(chat_config_dict, 'autogen_group_chat')
                result['group_chats'][chat_id] = chat_config
            except ConfigValidationError as e:
                validation_errors.append(f"Group chat '{chat_id}': {str(e)}")
            except Exception as e:
                validation_errors.append(f"Group chat '{chat_id}': Unexpected error: {str(e)}")
        
        # Load tool configurations
        for tool_id, tool_config_dict in config_dict.get('tools', {}).items():
            try:
                tool_config = ConfigLoader.load_from_dict(tool_config_dict, 'autogen_tool')
                result['tools'][tool_id] = tool_config
            except ConfigValidationError as e:
                validation_errors.append(f"Tool '{tool_id}': {str(e)}")
            except Exception as e:
                validation_errors.append(f"Tool '{tool_id}': Unexpected error: {str(e)}")
        
        # If there were any validation errors, raise an exception
        if validation_errors:
            raise ConfigValidationError("Invalid Autogen configuration", validation_errors)
        
        return result
