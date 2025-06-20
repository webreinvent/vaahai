"""
LLM client utilities for VaahAI.

This module provides utility functions for working with LLM clients,
including creating and configuring clients for different providers.
"""

import logging
from typing import Any, Dict, Optional

# Setup logging
logger = logging.getLogger(__name__)

def get_llm_client(provider: str) -> Any:
    """
    Get an LLM client for the specified provider.
    
    This function creates and returns an appropriate LLM client based on the
    provider name. It handles the configuration and initialization of the client
    using the VaahAI configuration system.
    
    Args:
        provider (str): The name of the LLM provider (e.g., "openai", "claude", "junie", "ollama")
        
    Returns:
        Any: An initialized LLM client for the specified provider
        
    Raises:
        ValueError: If the provider is not supported
    """
    logger.debug(f"Creating LLM client for provider: {provider}")
    
    try:
        # Import here to avoid circular imports
        from vaahai.config.manager import ConfigManager
        
        # Get the configuration manager
        config_manager = ConfigManager()
        
        # Check if the provider is supported
        if provider.lower() not in ["openai", "claude", "junie", "ollama"]:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        # Create a simple client wrapper that provides a consistent interface
        # for different LLM providers
        return LLMClientWrapper(provider, config_manager)
        
    except ImportError as e:
        logger.error(f"Failed to import required modules for LLM client: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create LLM client for {provider}: {e}")
        raise


class LLMClientWrapper:
    """
    A wrapper class that provides a consistent interface for different LLM providers.
    
    This class handles the provider-specific details of making API calls and
    processing responses, providing a unified interface for the rest of the
    application.
    """
    
    def __init__(self, provider: str, config_manager: Any):
        """
        Initialize the LLM client wrapper.
        
        Args:
            provider (str): The name of the LLM provider
            config_manager: The VaahAI configuration manager
        """
        self.provider = provider.lower()
        self.config_manager = config_manager
        
        # Get API key from configuration
        self.api_key = self._get_api_key()
        
        # Get default model for the provider
        self.model = self._get_default_model()
        
        logger.debug(f"Initialized LLM client for {provider} with model {self.model}")
    
    def _get_api_key(self) -> str:
        """
        Get the API key for the provider from configuration.
        
        Returns:
            str: The API key
            
        Raises:
            ValueError: If the API key is not configured
        """
        # Import here to avoid circular imports
        from vaahai.config.llm_utils import get_api_key_from_env
        
        # Try to get the API key from environment variables
        api_key = get_api_key_from_env(self.provider)
        
        if not api_key:
            # If not found in environment, try to get from configuration
            try:
                if self.provider == "openai":
                    api_key = self.config_manager.get_openai_api_key()
                elif self.provider == "claude":
                    api_key = self.config_manager.get_claude_api_key()
                elif self.provider == "junie":
                    api_key = self.config_manager.get_junie_api_key()
                # Ollama doesn't require an API key
            except Exception as e:
                logger.warning(f"Failed to get API key from configuration: {e}")
        
        if not api_key and self.provider != "ollama":
            logger.warning(f"No API key found for {self.provider}")
            raise ValueError(f"No API key configured for {self.provider}")
            
        return api_key
    
    def _get_default_model(self) -> str:
        """
        Get the default model for the provider.
        
        Returns:
            str: The default model name
        """
        # Import here to avoid circular imports
        from vaahai.config.llm_utils import get_default_model
        
        try:
            return get_default_model(self.provider)
        except Exception as e:
            logger.warning(f"Failed to get default model: {e}")
            
            # Fallback default models
            if self.provider == "openai":
                return "gpt-4"
            elif self.provider == "claude":
                return "claude-3-opus-20240229"
            elif self.provider == "junie":
                return "junie-8b"
            elif self.provider == "ollama":
                return "llama2"
            else:
                return "unknown"
    
    def complete(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion for the given prompt.
        
        Args:
            prompt (str): The prompt to generate a completion for
            **kwargs: Additional arguments to pass to the provider's API
            
        Returns:
            str: The generated completion
            
        Raises:
            Exception: If the completion fails
        """
        logger.debug(f"Generating completion with {self.provider} for prompt: {prompt[:50]}...")
        
        try:
            if self.provider == "openai":
                return self._complete_openai(prompt, **kwargs)
            elif self.provider == "claude":
                return self._complete_claude(prompt, **kwargs)
            elif self.provider == "junie":
                return self._complete_junie(prompt, **kwargs)
            elif self.provider == "ollama":
                return self._complete_ollama(prompt, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.error(f"Failed to generate completion: {e}")
            raise
    
    def _complete_openai(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion using the OpenAI API.
        
        Args:
            prompt (str): The prompt to generate a completion for
            **kwargs: Additional arguments to pass to the OpenAI API
            
        Returns:
            str: The generated completion
        """
        try:
            import openai
            
            # Configure the client
            openai.api_key = self.api_key
            
            # Set default parameters
            params = {
                "model": kwargs.get("model", self.model),
                "temperature": kwargs.get("temperature", 0.1),
                "max_tokens": kwargs.get("max_tokens", 1000),
            }
            
            # Create messages
            messages = [{"role": "user", "content": prompt}]
            
            # Make the API call
            response = openai.chat.completions.create(
                messages=messages,
                **params
            )
            
            # Extract and return the completion
            return response.choices[0].message.content
            
        except ImportError:
            logger.error("OpenAI package not installed. Install it with 'pip install openai'")
            raise
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _complete_claude(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion using the Anthropic Claude API.
        
        Args:
            prompt (str): The prompt to generate a completion for
            **kwargs: Additional arguments to pass to the Claude API
            
        Returns:
            str: The generated completion
        """
        try:
            import anthropic
            
            # Configure the client
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Set default parameters
            params = {
                "model": kwargs.get("model", self.model),
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.1),
            }
            
            # Make the API call
            response = client.messages.create(
                messages=[{"role": "user", "content": prompt}],
                **params
            )
            
            # Extract and return the completion
            return response.content[0].text
            
        except ImportError:
            logger.error("Anthropic package not installed. Install it with 'pip install anthropic'")
            raise
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    def _complete_junie(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion using the Junie API.
        
        Args:
            prompt (str): The prompt to generate a completion for
            **kwargs: Additional arguments to pass to the Junie API
            
        Returns:
            str: The generated completion
        """
        # Junie implementation would go here
        # This is a placeholder as Junie may not be a real provider
        logger.warning("Junie provider not implemented")
        return f"[JUNIE COMPLETION PLACEHOLDER] Response to: {prompt[:30]}..."
    
    def _complete_ollama(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion using the Ollama API.
        
        Args:
            prompt (str): The prompt to generate a completion for
            **kwargs: Additional arguments to pass to the Ollama API
            
        Returns:
            str: The generated completion
        """
        try:
            import requests
            
            # Set default parameters
            model = kwargs.get("model", self.model)
            
            # Ollama API endpoint (default is localhost)
            endpoint = kwargs.get("endpoint", "http://localhost:11434")
            
            # Make the API call
            response = requests.post(
                f"{endpoint}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "temperature": kwargs.get("temperature", 0.1),
                    "max_tokens": kwargs.get("max_tokens", 1000),
                }
            )
            
            # Check for errors
            response.raise_for_status()
            
            # Extract and return the completion
            return response.json().get("response", "")
            
        except ImportError:
            logger.error("Requests package not installed. Install it with 'pip install requests'")
            raise
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
