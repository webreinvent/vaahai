"""
LLM provider utilities for VaahAI.

This module provides utility functions for working with LLM providers,
including listing available providers and models, validating API keys,
and getting default models.
"""

import os
from typing import List, Dict, Any, Optional

from vaahai.config.schema import (
    OPENAI_MODELS,
    CLAUDE_MODELS,
    JUNIE_MODELS,
    OLLAMA_MODELS,
)


# Available LLM providers
PROVIDERS = ["openai", "claude", "junie", "ollama"]


def list_providers() -> List[str]:
    """
    List all available LLM providers.
    
    Returns:
        List[str]: List of provider names
    """
    return PROVIDERS


def list_models(provider: str) -> List[str]:
    """
    List available models for a provider.
    
    Args:
        provider (str): Provider name
        
    Returns:
        List[str]: List of model names
        
    Raises:
        ValueError: If provider is not supported
    """
    if provider == "openai":
        return OPENAI_MODELS
    elif provider == "claude":
        return CLAUDE_MODELS
    elif provider == "junie":
        return JUNIE_MODELS
    elif provider == "ollama":
        return OLLAMA_MODELS
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def get_default_model(provider: str) -> str:
    """
    Get the default model for a provider.
    
    Args:
        provider (str): Provider name
        
    Returns:
        str: Default model name
        
    Raises:
        ValueError: If provider is not supported
    """
    if provider == "openai":
        return "gpt-4"
    elif provider == "claude":
        return "claude-3-sonnet-20240229"
    elif provider == "junie":
        return "junie-8b"
    elif provider == "ollama":
        return "llama3"
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def validate_api_key(provider: str, api_key: str) -> bool:
    """
    Validate an API key for a provider.
    
    This is a basic validation that checks if the API key is not empty.
    For actual validation, you would need to make an API call to the provider,
    which is not implemented here to avoid unnecessary API calls.
    
    Args:
        provider (str): Provider name
        api_key (str): API key to validate
        
    Returns:
        bool: True if the API key is valid, False otherwise
    """
    # Basic validation - check if API key is not empty
    if not api_key:
        return False
    
    # For a more comprehensive validation, you could make a test API call
    # to the provider, but that would require additional dependencies and
    # could incur costs. This is left as a future enhancement.
    
    return True


def get_api_key_from_env(provider: str) -> Optional[str]:
    """
    Get API key from environment variables.
    
    Checks for environment variables in the following order:
    1. VAAHAI_{PROVIDER}_API_KEY (e.g., VAAHAI_OPENAI_API_KEY)
    2. {PROVIDER}_API_KEY (e.g., OPENAI_API_KEY)
    
    Args:
        provider (str): Provider name
        
    Returns:
        Optional[str]: API key if found, None otherwise
    """
    provider_upper = provider.upper()
    
    # Check for VAAHAI_{PROVIDER}_API_KEY
    env_var = f"VAAHAI_{provider_upper}_API_KEY"
    api_key = os.environ.get(env_var)
    if api_key:
        return api_key
    
    # Check for {PROVIDER}_API_KEY
    env_var = f"{provider_upper}_API_KEY"
    api_key = os.environ.get(env_var)
    if api_key:
        return api_key
    
    return None


def get_provider_config_path(provider: str) -> str:
    """
    Get the configuration path for a provider in dot notation.
    
    Args:
        provider (str): Provider name
        
    Returns:
        str: Configuration path in dot notation
        
    Raises:
        ValueError: If provider is not supported
    """
    if provider in PROVIDERS:
        return f"llm.{provider}"
    else:
        raise ValueError(f"Unsupported provider: {provider}")
