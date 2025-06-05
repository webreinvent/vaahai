#!/usr/bin/env python
"""
Example script demonstrating how to use the ConfigLoader class.

This script shows how to load configurations from files, dictionaries, and JSON strings,
and how to handle environment variable substitution and validation errors.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaahai.agents.config_loader import (
    ConfigLoader,
    ConfigLoadError,
    ConfigValidationError
)


def load_from_file_example():
    """Example of loading configuration from a file."""
    print("\n=== Loading Configuration from File ===")
    
    config_path = os.path.join(os.path.dirname(__file__), 'autogen_config_example.json')
    
    try:
        # Load the entire Autogen configuration
        print("Loading complete Autogen configuration...")
        autogen_config = ConfigLoader.load_autogen_config(config_path)
        
        print(f"Successfully loaded {len(autogen_config['agents'])} agents, "
              f"{len(autogen_config['group_chats'])} group chats, and "
              f"{len(autogen_config['tools'])} tools.")
        
        # Load a specific agent configuration
        print("\nLoading a specific agent configuration...")
        config_dict = ConfigLoader.load_from_file(config_path)
        agent_config = ConfigLoader.load_from_dict(config_dict['agents']['assistant'], 'autogen_agent')
        
        print(f"Agent name: {agent_config.get('name')}")
        print(f"System message: {agent_config.get('system_message')}")
        
        # Access nested configuration
        llm_config = agent_config.get('llm_config', {})
        if llm_config:
            config_list = llm_config.get('config_list', [])
            if config_list:
                print(f"Model: {config_list[0].get('model')}")
                print(f"Temperature: {llm_config.get('temperature')}")
    
    except ConfigLoadError as e:
        print(f"Error loading configuration: {e}")
    except ConfigValidationError as e:
        print(f"Configuration validation error: {e}")


def load_from_dict_example():
    """Example of loading configuration from a dictionary."""
    print("\n=== Loading Configuration from Dictionary ===")
    
    # Create a dictionary with environment variable placeholders
    agent_config = {
        "name": "DictAgent",
        "system_message": "You are an agent created from a dictionary",
        "human_input_mode": "NEVER",
        "llm_config": {
            "config_list": [
                {
                    "model": "${MODEL_NAME}",
                    "api_key": "${OPENAI_API_KEY}",
                    "api_type": "openai"
                }
            ],
            "temperature": 0.5
        }
    }
    
    # Set environment variables for testing
    os.environ["MODEL_NAME"] = "gpt-4"
    os.environ["OPENAI_API_KEY"] = "sk-example-key"
    
    try:
        # Substitute environment variables
        agent_config = ConfigLoader.substitute_env_vars(agent_config)
        
        # Load and validate the configuration
        config = ConfigLoader.load_from_dict(agent_config, "autogen_agent")
        
        print(f"Agent name: {config.get('name')}")
        print(f"System message: {config.get('system_message')}")
        
        # Access nested configuration with environment variables substituted
        llm_config = config.get('llm_config', {})
        if llm_config:
            config_list = llm_config.get('config_list', [])
            if config_list:
                print(f"Model: {config_list[0].get('model')}")  # Should be "gpt-4"
                print(f"API key: {config_list[0].get('api_key')}")  # Should be "sk-example-key"
    
    except ConfigValidationError as e:
        print(f"Configuration validation error: {e}")


def load_from_json_string_example():
    """Example of loading configuration from a JSON string."""
    print("\n=== Loading Configuration from JSON String ===")
    
    # Create a JSON string
    json_string = '''
    {
        "model": "gpt-4",
        "api_key": "${OPENAI_API_KEY}",
        "api_type": "openai",
        "organization": "my-org"
    }
    '''
    
    try:
        # Load and validate the configuration
        config = ConfigLoader.load_from_json_string(json_string, "llm")
        
        print(f"Model: {config.get('model')}")
        print(f"API key: {config.get('api_key')}")  # Should have environment variable substituted
        print(f"API type: {config.get('api_type')}")
        print(f"Organization: {config.get('organization')}")
    
    except ConfigLoadError as e:
        print(f"Error loading configuration: {e}")
    except ConfigValidationError as e:
        print(f"Configuration validation error: {e}")


def handle_validation_errors_example():
    """Example of handling validation errors."""
    print("\n=== Handling Validation Errors ===")
    
    # Create an invalid configuration (missing required fields)
    invalid_config = {
        "name": "InvalidAgent"
        # Missing required "system_message" field
    }
    
    try:
        ConfigLoader.load_from_dict(invalid_config, "autogen_agent")
    except ConfigValidationError as e:
        print(f"Caught validation error: {e}")
        
        # In a real application, you might want to provide more helpful error messages
        print("\nSuggested fix: Add the required 'system_message' field to the configuration.")


def main():
    """Main function."""
    print("ConfigLoader Examples")
    print("====================")
    
    # Run examples
    load_from_file_example()
    load_from_dict_example()
    load_from_json_string_example()
    handle_validation_errors_example()
    
    print("\nAll examples completed.")


if __name__ == "__main__":
    main()
