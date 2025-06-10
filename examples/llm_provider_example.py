#!/usr/bin/env python3
"""
Example script demonstrating how to use the LLM provider configuration.

This script shows how to:
1. Get the current LLM provider
2. List available providers and models
3. Set the active provider
4. Get and set API keys
5. Get and set models
6. Access provider-specific configuration
"""

import os
from pathlib import Path
from vaahai.config.manager import ConfigManager
from vaahai.config.llm_utils import list_providers, list_models

# Create a config manager
config_manager = ConfigManager()

# Print header
print("VaahAI LLM Provider Configuration Example")
print("=" * 40)

# 1. Get the current LLM provider
current_provider = config_manager.get_current_provider()
print(f"Current LLM provider: {current_provider}")

# 2. List available providers and models
print("\nAvailable LLM providers:")
for provider in list_providers():
    print(f"- {provider}")

print("\nAvailable models for current provider:")
for model in list_models(current_provider):
    if model == config_manager.get_model():
        print(f"- {model} (current)")
    else:
        print(f"- {model}")

# 3. Set the active provider
print("\nChanging provider to Claude...")
config_manager.set_provider("claude")
print(f"Current provider is now: {config_manager.get_current_provider()}")

# 4. Get and set API keys
print("\nAPI Key Management:")
api_key = config_manager.get_api_key()
if api_key:
    print(f"API key for {config_manager.get_current_provider()}: {api_key[:5]}...")
else:
    print(f"No API key set for {config_manager.get_current_provider()}")

# Example of setting an API key (commented out for safety)
# config_manager.set_api_key("your-api-key-here")
print("To set an API key, use: config_manager.set_api_key('your-api-key-here')")

# 5. Get and set models
current_model = config_manager.get_model()
print(f"\nCurrent model for {config_manager.get_current_provider()}: {current_model}")

# List available models for current provider
print("\nAvailable models for current provider:")
for model in list_models(config_manager.get_current_provider()):
    if model == current_model:
        print(f"- {model} (current)")
    else:
        print(f"- {model}")

# Set a different model
try:
    print("\nChanging model...")
    new_model = "claude-3-opus-20240229"
    config_manager.set_model(new_model)
    print(f"Model changed to: {config_manager.get_model()}")
except ValueError as e:
    print(f"Error setting model: {e}")

# 6. Access provider-specific configuration
print("\nProvider-specific configuration:")
provider_config = config_manager.get_provider_config()
for key, value in provider_config.items():
    if key == "api_key" and value:
        print(f"- {key}: {value[:5]}...")
    else:
        print(f"- {key}: {value}")

# Save the configuration
print("\nSaving configuration...")
if config_manager.save():
    print("Configuration saved successfully")
else:
    print("Failed to save configuration")

# Environment variable overrides
print("\nEnvironment variable overrides:")
print("You can override configuration with environment variables:")
print("  VAAHAI_LLM_PROVIDER=openai")
print("  VAAHAI_LLM_OPENAI_API_KEY=your-api-key")
print("  VAAHAI_LLM_OPENAI_MODEL=gpt-4")

# Example of using environment variables
print("\nExample with environment variables:")
os.environ["VAAHAI_LLM_PROVIDER"] = "openai"
new_config_manager = ConfigManager()
print(f"Provider from environment: {new_config_manager.get_current_provider()}")

# Cleanup
del os.environ["VAAHAI_LLM_PROVIDER"]

print("\nExample completed!")
