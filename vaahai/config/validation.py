"""
Configuration validation utility for VaahAI.

This module provides utilities for validating VaahAI configuration,
ensuring that the configuration is complete and valid before running commands.
"""

from typing import Dict, Any, List, Optional, Tuple
import os
from pathlib import Path

from vaahai.config.schema import (
    validate_config, 
    PROVIDER_MODEL_INFO,
    MODEL_CAPABILITY_TEXT,
    MODEL_CAPABILITY_CODE
)
from vaahai.config.manager import ConfigManager


class ConfigValidationError(Exception):
    """Exception raised for configuration validation errors."""
    pass


def validate_provider_setup(config: Dict[str, Any], provider: str) -> List[str]:
    """
    Validate provider-specific configuration.
    
    Args:
        config: Configuration dictionary
        provider: Provider to validate
        
    Returns:
        List of validation errors
    """
    errors = []
    
    # Check if provider exists in config
    if provider not in ["openai", "claude", "junie", "ollama"]:
        errors.append(f"Invalid provider: {provider}")
        return errors
        
    # Check if provider config exists
    if provider not in config.get("llm", {}):
        errors.append(f"Missing configuration for provider: {provider}")
        return errors
    
    provider_config = config["llm"][provider]
    
    # Check API key for providers that require it
    if provider != "ollama" and not provider_config.get("api_key"):
        errors.append(f"Missing API key for {provider}")
    
    # Check model
    model = provider_config.get("model", "")
    if not model:
        errors.append(f"No model selected for {provider}")
    else:
        # Check if model is valid for provider
        valid_models = [model_info[0] for model_info in PROVIDER_MODEL_INFO.get(provider, [])]
        if model not in valid_models:
            errors.append(f"Invalid model '{model}' for {provider}")
    
    # Check API base for Ollama
    if provider == "ollama" and not provider_config.get("api_base"):
        errors.append("Missing API base URL for Ollama")
    
    return errors


def check_model_capabilities(provider: str, model: str, required_capabilities: List[str]) -> Tuple[bool, List[str]]:
    """
    Check if the selected model has the required capabilities.
    
    Args:
        provider: LLM provider
        model: Model name
        required_capabilities: List of required capabilities
        
    Returns:
        Tuple of (is_valid, missing_capabilities)
    """
    missing_capabilities = []
    
    # Find model info
    model_info_list = PROVIDER_MODEL_INFO.get(provider, [])
    model_info = next((info for info in model_info_list if info[0] == model), None)
    
    if not model_info:
        return False, ["unknown_model"]
    
    # Check capabilities
    model_capabilities = model_info[1]
    for capability in required_capabilities:
        if capability not in model_capabilities:
            missing_capabilities.append(capability)
    
    return len(missing_capabilities) == 0, missing_capabilities


def validate_configuration_exists() -> Tuple[bool, str]:
    """
    Check if VaahAI configuration exists.
    
    Returns:
        Tuple of (exists, message)
    """
    try:
        config_manager = ConfigManager()
        if not config_manager.exists():
            return False, "VaahAI configuration not found. Run 'vaahai config init' to set up."
        return True, "Configuration exists"
    except Exception as e:
        return False, f"Error accessing configuration: {str(e)}"


def validate_configuration_complete() -> List[str]:
    """
    Validate that the VaahAI configuration is complete and valid.
    
    Returns:
        List of validation errors
    """
    errors = []
    
    # Check if configuration exists
    exists, message = validate_configuration_exists()
    if not exists:
        errors.append(message)
        return errors
    
    try:
        # Get configuration
        config_manager = ConfigManager()
        config = config_manager.get_full_config()
        
        # Run schema validation
        schema_errors = validate_config(config)
        errors.extend(schema_errors)
        
        # Check active provider setup
        provider = config.get("llm", {}).get("provider", "")
        if provider:
            provider_errors = validate_provider_setup(config, provider)
            errors.extend(provider_errors)
        else:
            errors.append("No LLM provider selected")
        
        # Check if Docker is properly configured when enabled
        if config.get("docker", {}).get("enabled", False):
            docker_config = config.get("docker", {})
            if not docker_config.get("image"):
                errors.append("Docker is enabled but no image is specified")
        
    except Exception as e:
        errors.append(f"Error validating configuration: {str(e)}")
    
    return errors


def validate_for_command(command: str) -> Tuple[bool, List[str]]:
    """
    Validate configuration for a specific command.
    
    Args:
        command: Command name to validate for
        
    Returns:
        Tuple of (is_valid, errors)
    """
    errors = validate_configuration_complete()
    
    # If we already have errors, no need to check further
    if errors:
        return False, errors
    
    try:
        config_manager = ConfigManager()
        config = config_manager.get_full_config()
        provider = config.get("llm", {}).get("provider", "")
        model = config.get("llm", {}).get(provider, {}).get("model", "")
        
        # Command-specific validations
        if command in ["review", "audit"]:
            # These commands require code generation capabilities
            valid, missing = check_model_capabilities(
                provider, model, [MODEL_CAPABILITY_TEXT, MODEL_CAPABILITY_CODE]
            )
            if not valid:
                if "unknown_model" in missing:
                    errors.append(f"Unknown model '{model}' for provider '{provider}'")
                else:
                    errors.append(
                        f"The selected model '{model}' does not support required capabilities: {', '.join(missing)}"
                    )
        
        # Add more command-specific validations as needed
        
    except Exception as e:
        errors.append(f"Error validating configuration for command '{command}': {str(e)}")
    
    return len(errors) == 0, errors


def get_validation_summary() -> Dict[str, Any]:
    """
    Get a summary of configuration validation status.
    
    Returns:
        Dictionary with validation summary
    """
    exists, message = validate_configuration_exists()
    errors = validate_configuration_complete() if exists else [message]
    
    # Get provider and model if configuration exists
    provider = ""
    model = ""
    if exists:
        try:
            config_manager = ConfigManager()
            provider = config_manager.get_current_provider()
            model = config_manager.get_model(provider)
        except Exception:
            pass
    
    return {
        "is_valid": len(errors) == 0,
        "exists": exists,
        "errors": errors,
        "provider": provider,
        "model": model,
        "error_count": len(errors)
    }
