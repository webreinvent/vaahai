"""
Configuration manager for VaahAI.

This module provides the ConfigManager class, which is responsible for loading,
saving, and accessing configuration values from multiple sources, including:
- Default configuration
- User configuration (~/.vaahai/config.toml)
- Project configuration (./.vaahai/config.toml)
- Environment variables
- Command-line options
"""

import os
import copy
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from vaahai.config.defaults import DEFAULT_CONFIG
from vaahai.config.loader import load_toml, save_toml
from vaahai.config.schema import validate_config, config_to_schema, schema_to_config, VaahAIConfig
from vaahai.config.utils import (
    get_user_config_dir,
    get_project_config_dir,
    ensure_config_dir,
    get_env_var,
    get_env_var_name,
    set_nested_value,
    get_nested_value,
)


class ConfigManager:
    """
    Manages VaahAI configuration.
    
    This class is responsible for loading, saving, and accessing configuration
    values from multiple sources, with a defined precedence order:
    1. Command-line options (highest precedence)
    2. Environment variables
    3. Project configuration
    4. User configuration
    5. Default configuration (lowest precedence)
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path (Optional[Path]): Optional path to a specific configuration file
        """
        self.user_config_dir = get_user_config_dir()
        self.project_config_dir = get_project_config_dir()
        self.config_path = config_path
        self.config = self._load_config()
        self.cli_overrides = {}
        self._schema = config_to_schema(self.config)

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from all sources.
        
        Returns:
            Dict[str, Any]: Merged configuration
        """
        # Start with defaults
        config = copy.deepcopy(DEFAULT_CONFIG)

        # Load user config
        user_config_path = self.user_config_dir / "config.toml"
        if user_config_path.exists():
            user_config = load_toml(user_config_path)
            self._merge_config(config, user_config)

        # Load project config if it exists
        project_config_path = self.project_config_dir / "config.toml"
        if project_config_path.exists():
            project_config = load_toml(project_config_path)
            self._merge_config(config, project_config)

        # Load from specified path if provided
        if self.config_path and self.config_path.exists():
            custom_config = load_toml(self.config_path)
            self._merge_config(config, custom_config)

        # Apply environment variable overrides
        self._apply_env_overrides(config)

        # Validate the configuration
        errors = validate_config(config)
        if errors:
            for error in errors:
                print(f"Configuration warning: {error}")

        return config

    def _merge_config(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> None:
        """
        Merge overlay config into base config.
        
        Args:
            base (Dict[str, Any]): Base configuration
            overlay (Dict[str, Any]): Overlay configuration to merge into base
        """
        for key, value in overlay.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _apply_env_overrides(self, config: Dict[str, Any]) -> None:
        """
        Apply environment variable overrides to config.
        
        This method checks for environment variables with the VAAHAI_ prefix
        and applies them to the configuration.
        
        Args:
            config (Dict[str, Any]): Configuration to update with environment variables
        """
        # Process all environment variables with VAAHAI_ prefix
        for env_key, env_value in os.environ.items():
            if env_key.startswith("VAAHAI_"):
                # Convert environment variable name to config key
                # e.g., VAAHAI_LLM_PROVIDER -> llm.provider
                config_key = env_key[7:].lower().replace("_", ".")
                set_nested_value(config, config_key, env_value)

    def apply_cli_overrides(self, overrides: Dict[str, Any]) -> None:
        """
        Apply command-line overrides to the configuration.
        
        Args:
            overrides (Dict[str, Any]): Dictionary of command-line overrides
        """
        self.cli_overrides = overrides.copy()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key in dot notation (e.g., "llm.provider")
            default (Any): Default value to return if key not found
        
        Returns:
            Any: Configuration value or default if not found
        """
        # Check CLI overrides first
        if key in self.cli_overrides:
            return self.cli_overrides[key]
            
        # Check environment variables
        env_var_name = get_env_var_name(key)
        env_value = os.environ.get(env_var_name)
        if env_value is not None:
            return env_value
            
        # Get from config
        return get_nested_value(self.config, key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key (str): Configuration key in dot notation (e.g., "llm.provider")
            value (Any): Value to set
        """
        set_nested_value(self.config, key, value)
        # Update schema representation
        self._schema = config_to_schema(self.config)

    def save(self, user_level: bool = True) -> bool:
        """
        Save the configuration.
        
        Args:
            user_level (bool): If True, save to user config, otherwise to project config
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate configuration before saving
        errors = validate_config(self.config)
        if errors:
            for error in errors:
                print(f"Configuration warning: {error}")
        
        if user_level:
            ensure_config_dir(self.user_config_dir)
            return save_toml(self.user_config_dir / "config.toml", self.config)
        else:
            ensure_config_dir(self.project_config_dir)
            return save_toml(self.project_config_dir / "config.toml", self.config)

    def reset(self) -> None:
        """
        Reset the configuration to defaults.
        """
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        self.cli_overrides = {}
        self._schema = config_to_schema(self.config)

    def exists(self, level: str = "user") -> bool:
        """
        Check if a configuration file exists.
        
        Args:
            level (str): Level to check ("user" or "project")
        
        Returns:
            bool: True if configuration file exists, False otherwise
        """
        if level == "user":
            return (self.user_config_dir / "config.toml").exists()
        elif level == "project":
            return (self.project_config_dir / "config.toml").exists()
        return False

    def get_full_config(self) -> Dict[str, Any]:
        """
        Get the full configuration dictionary.
        
        Returns:
            Dict[str, Any]: Full configuration dictionary
        """
        # Create a copy to avoid modifying the original
        config = copy.deepcopy(self.config)
        
        # Apply CLI overrides
        for key, value in self.cli_overrides.items():
            set_nested_value(config, key, value)
            
        # Apply environment variable overrides
        for env_key, env_value in os.environ.items():
            if env_key.startswith("VAAHAI_"):
                config_key = env_key[7:].lower().replace("_", ".")
                set_nested_value(config, config_key, env_value)
                
        return config

    def get_schema(self) -> VaahAIConfig:
        """
        Get the configuration as a schema object.
        
        Returns:
            VaahAIConfig: Configuration as a schema object
        """
        return config_to_schema(self.get_full_config())

    def validate(self) -> List[str]:
        """
        Validate the current configuration.
        
        Returns:
            List[str]: List of validation errors, empty if valid
        """
        return validate_config(self.get_full_config())
