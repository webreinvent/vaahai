#!/usr/bin/env python
"""
Example script demonstrating how to load and use Autogen configurations.

This script shows how to load Autogen configurations from a JSON file,
validate them, and use them to create agents and group chats.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vaahai.agents.config import (
    ConfigFactory,
    AutogenAgentConfig,
    AutogenGroupChatConfig,
    AutogenToolConfig
)


def load_config_from_file(file_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the configuration
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def process_environment_variables(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process environment variables in the configuration.
    
    Args:
        config_dict: Dictionary containing the configuration
        
    Returns:
        Dictionary with environment variables replaced
    """
    import json
    config_str = json.dumps(config_dict)
    
    # Replace environment variables
    import re
    import os
    
    def replace_env_var(match):
        env_var = match.group(1)
        return os.environ.get(env_var, f"${{{env_var}}}")
    
    config_str = re.sub(r'\$\{([^}]+)\}', replace_env_var, config_str)
    return json.loads(config_str)


def main():
    """Main function."""
    print("Loading Autogen configuration example...")
    
    # Load configuration from file
    config_path = os.path.join(os.path.dirname(__file__), 'autogen_config_example.json')
    config = load_config_from_file(config_path)
    
    # Process environment variables
    config = process_environment_variables(config)
    
    # Create agent configurations
    agent_configs = {}
    for agent_id, agent_config_dict in config.get('agents', {}).items():
        agent_config = ConfigFactory.from_dict('autogen_agent', agent_config_dict)
        if agent_config.validate():
            agent_configs[agent_id] = agent_config
            print(f"✓ Valid agent configuration: {agent_id}")
        else:
            print(f"✗ Invalid agent configuration: {agent_id}")
    
    # Create group chat configurations
    group_chat_configs = {}
    for chat_id, chat_config_dict in config.get('group_chats', {}).items():
        chat_config = ConfigFactory.from_dict('autogen_group_chat', chat_config_dict)
        if chat_config.validate():
            group_chat_configs[chat_id] = chat_config
            print(f"✓ Valid group chat configuration: {chat_id}")
        else:
            print(f"✗ Invalid group chat configuration: {chat_id}")
    
    # Create tool configurations
    tool_configs = {}
    for tool_id, tool_config_dict in config.get('tools', {}).items():
        tool_config = ConfigFactory.from_dict('autogen_tool', tool_config_dict)
        if tool_config.validate():
            tool_configs[tool_id] = tool_config
            print(f"✓ Valid tool configuration: {tool_id}")
        else:
            print(f"✗ Invalid tool configuration: {tool_id}")
    
    # Print summary
    print("\nConfiguration Summary:")
    print(f"- Agents: {len(agent_configs)}")
    print(f"- Group Chats: {len(group_chat_configs)}")
    print(f"- Tools: {len(tool_configs)}")
    
    # Example: Access configuration values
    if 'assistant' in agent_configs:
        assistant_config = agent_configs['assistant']
        print(f"\nAssistant System Message: {assistant_config.get('system_message')}")
        
        llm_config = assistant_config.get('llm_config', {})
        config_list = llm_config.get('config_list', [])
        if config_list:
            model = config_list[0].get('model', 'unknown')
            print(f"Assistant Model: {model}")


if __name__ == "__main__":
    main()
