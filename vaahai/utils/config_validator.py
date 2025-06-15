"""
VaahAI configuration validation utility.

This module provides utilities for validating VaahAI configuration,
including checks for config directory existence, required files,
and essential configuration values.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union

from vaahai.config.manager import ConfigManager
from vaahai.config.utils import (
    get_user_config_dir,
    get_project_config_dir,
    ensure_config_dir,
)


class ValidationLevel(Enum):
    """Validation severity levels for configuration validation."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationResult:
    """
    Result of a configuration validation check.
    
    Attributes:
        level (ValidationLevel): Severity level of the validation result
        message (str): Descriptive message about the validation result
        key (Optional[str]): Configuration key related to this validation
        valid (bool): Whether the validation passed
    """
    
    def __init__(
        self,
        level: ValidationLevel,
        message: str,
        key: Optional[str] = None,
        valid: bool = False,
    ):
        self.level = level
        self.message = message
        self.key = key
        self.valid = valid
    
    def __str__(self) -> str:
        prefix = "✅" if self.valid else "❌"
        key_str = f" [{self.key}]" if self.key else ""
        return f"{prefix} {self.level.value.upper()}{key_str}: {self.message}"


class ConfigValidator:
    """
    Validates VaahAI configuration.
    
    This class checks for proper VaahAI configuration, including:
    - Config directory existence
    - Required configuration files
    - Essential configuration values
    - API key validation
    """
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        strict: bool = False,
    ):
        """
        Initialize the configuration validator.
        
        Args:
            config_path (Optional[Path]): Path to a specific configuration file
            strict (bool): Whether validation should be strict (all errors are critical)
        """
        self.config_path = config_path
        self.strict = strict
        self.user_config_dir = get_user_config_dir()
        self.project_config_dir = get_project_config_dir()
        
        try:
            self.config_manager = ConfigManager(config_path)
        except Exception:
            # Will validate config existence separately
            self.config_manager = None
    
    def validate(self) -> Tuple[bool, List[ValidationResult]]:
        """
        Validate the VaahAI configuration.
        
        Returns:
            Tuple[bool, List[ValidationResult]]: Validation success status and detailed results
        """
        results = []
        
        # Check config directories
        results.extend(self._validate_config_directories())
        
        # If user config doesn't exist, we can't continue with config validation
        if not any(r.valid for r in results if r.key == "user_config_dir"):
            results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    "VaahAI is not configured. Run 'vaahai config init' to set it up.",
                    key="config_init",
                    valid=False,
                )
            )
            return False, results
        
        # Check config files
        results.extend(self._validate_config_files())
        
        # If config files don't exist, we can't continue with content validation
        if not any(r.valid for r in results if r.key == "user_config_file"):
            results.append(
                ValidationResult(
                    ValidationLevel.ERROR,
                    "VaahAI configuration file not found. Run 'vaahai config init' to set it up.",
                    key="config_file",
                    valid=False,
                )
            )
            return False, results
        
        # Check config content
        results.extend(self._validate_config_content())
        
        # Determine overall validation status
        is_valid = all(r.valid or r.level != ValidationLevel.ERROR for r in results)
        
        return is_valid, results
    
    def _validate_config_directories(self) -> List[ValidationResult]:
        """
        Validate that required configuration directories exist.
        
        Returns:
            List[ValidationResult]: Validation results for config directories
        """
        results = []
        
        # Check user config directory
        user_dir_exists = self.user_config_dir.exists()
        results.append(
            ValidationResult(
                ValidationLevel.ERROR if not user_dir_exists else ValidationLevel.INFO,
                f"User config directory {'exists' if user_dir_exists else 'does not exist'} at {self.user_config_dir}",
                key="user_config_dir",
                valid=user_dir_exists,
            )
        )
        
        # Check project config directory (warning only, not required)
        project_dir_exists = self.project_config_dir.exists()
        results.append(
            ValidationResult(
                ValidationLevel.WARNING if not project_dir_exists else ValidationLevel.INFO,
                f"Project config directory {'exists' if project_dir_exists else 'does not exist'} at {self.project_config_dir}",
                key="project_config_dir",
                valid=project_dir_exists,
            )
        )
        
        return results
    
    def _validate_config_files(self) -> List[ValidationResult]:
        """
        Validate that required configuration files exist.
        
        Returns:
            List[ValidationResult]: Validation results for config files
        """
        results = []
        
        # Check user config file
        user_config_file = self.user_config_dir / "config.toml"
        user_file_exists = user_config_file.exists()
        results.append(
            ValidationResult(
                ValidationLevel.ERROR if not user_file_exists else ValidationLevel.INFO,
                f"User config file {'exists' if user_file_exists else 'does not exist'} at {user_config_file}",
                key="user_config_file",
                valid=user_file_exists,
            )
        )
        
        # Check project config file (warning only, not required)
        project_config_file = self.project_config_dir / "config.toml"
        project_file_exists = project_config_file.exists()
        results.append(
            ValidationResult(
                ValidationLevel.WARNING if not project_file_exists else ValidationLevel.INFO,
                f"Project config file {'exists' if project_file_exists else 'does not exist'} at {project_config_file}",
                key="project_config_file",
                valid=project_file_exists,
            )
        )
        
        return results
    
    def _validate_config_content(self) -> List[ValidationResult]:
        """
        Validate the content of the configuration.
        
        Returns:
            List[ValidationResult]: Validation results for config content
        """
        results = []
        
        if not self.config_manager:
            # This shouldn't happen if we've validated config files first
            return [
                ValidationResult(
                    ValidationLevel.ERROR,
                    "Could not load configuration manager",
                    key="config_manager",
                    valid=False,
                )
            ]
        
        # Check if provider is set
        provider = self.config_manager.get_current_provider()
        provider_valid = provider is not None and provider != ""
        results.append(
            ValidationResult(
                ValidationLevel.ERROR if not provider_valid else ValidationLevel.INFO,
                f"LLM provider {'is' if provider_valid else 'is not'} configured{f' as {provider}' if provider_valid else ''}",
                key="llm.provider",
                valid=provider_valid,
            )
        )
        
        # Check if model is set
        if provider_valid:
            model = self.config_manager.get_model(provider)
            model_valid = model is not None and model != ""
            results.append(
                ValidationResult(
                    ValidationLevel.ERROR if not model_valid else ValidationLevel.INFO,
                    f"LLM model {'is' if model_valid else 'is not'} configured{f' as {model}' if model_valid else ''}",
                    key=f"llm.{provider}.model",
                    valid=model_valid,
                )
            )
            
            # Check if API key is set
            api_key = self.config_manager.get_api_key(provider)
            api_key_valid = api_key is not None and api_key != ""
            results.append(
                ValidationResult(
                    ValidationLevel.ERROR if not api_key_valid else ValidationLevel.INFO,
                    f"API key for {provider} {'is' if api_key_valid else 'is not'} configured",
                    key=f"llm.{provider}.api_key",
                    valid=api_key_valid,
                )
            )
        
        return results
    
    @staticmethod
    def is_configured() -> bool:
        """
        Check if VaahAI is configured at all.
        
        This is a simple check to determine if the configuration has been initialized.
        It doesn't validate the configuration content, just checks if the basic files exist.
        
        Returns:
            bool: True if VaahAI appears to be configured, False otherwise
        """
        user_config_dir = get_user_config_dir()
        user_config_file = user_config_dir / "config.toml"
        return user_config_dir.exists() and user_config_file.exists()
