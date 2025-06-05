# VaahAI Autogen Configuration Guide

This guide explains how to use the Autogen configuration system in VaahAI, including how to define, load, validate, and use configurations for agents, group chats, and tools.

## Table of Contents
- [Configuration Overview](#configuration-overview)
- [Configuration Schema](#configuration-schema)
- [ConfigLoader](#configloader)
- [Environment Variable Substitution](#environment-variable-substitution)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Configuration Overview

The VaahAI Autogen configuration system provides a structured way to define and manage configurations for:

- **Agents**: AI assistants with specific roles and capabilities
- **Group Chats**: Conversations involving multiple agents
- **Tools**: Functions that agents can use to perform tasks

Configurations can be loaded from various sources:
- JSON files
- Python dictionaries
- JSON strings

## Configuration Schema

Each configuration type has a specific schema that defines its required and optional fields:

### LLM Configuration

```json
{
  "model": "gpt-4",
  "api_key": "${OPENAI_API_KEY}",
  "api_type": "openai",
  "organization": "my-org"
}
```

Required fields:
- `model`: The model name to use

Optional fields depend on the `api_type`:
- For `openai`: `api_key`, `organization`
- For `azure`: `api_key`, `api_version`, `base_url`
- For `custom`: `api_key` and any other fields needed by the custom API

### Agent Configuration

```json
{
  "name": "Assistant",
  "system_message": "You are a helpful AI assistant.",
  "human_input_mode": "NEVER",
  "llm_config": {
    "config_list": [
      {
        "model": "gpt-4",
        "api_key": "${OPENAI_API_KEY}",
        "api_type": "openai"
      }
    ],
    "temperature": 0.7
  }
}
```

Required fields:
- `name`: Agent name
- `system_message`: Instructions for the agent

Optional fields:
- `human_input_mode`: When to request human input (`ALWAYS`, `NEVER`, or `TERMINATE`)
- `max_consecutive_auto_reply`: Maximum number of consecutive auto-replies
- `llm_config`: LLM configuration for the agent
- `code_execution_config`: Configuration for code execution
- `is_termination_msg`: Function to determine if a message should terminate the conversation
- `function_map`: Map of function names to callable functions

### Group Chat Configuration

```json
{
  "name": "ProblemSolving",
  "agents": ["assistant", "coder", "critic"],
  "max_round": 10
}
```

Required fields:
- `name`: Group chat name
- `agents`: List of agent names participating in the chat

Optional fields:
- `max_round`: Maximum number of conversation rounds
- `messages`: Initial messages in the conversation
- `speaker_selection_method`: Method for selecting the next speaker

### Tool Configuration

```json
{
  "name": "Calculator",
  "description": "Performs mathematical calculations",
  "parameters": {
    "expression": {
      "type": "string",
      "description": "Mathematical expression to evaluate"
    }
  }
}
```

Required fields:
- `name`: Tool name
- `description`: Tool description
- `parameters`: Tool parameters schema

## ConfigLoader

The `ConfigLoader` class provides methods for loading configurations from various sources and validating them against schemas.

### Loading from a Dictionary

```python
from vaahai.agents.config_loader import ConfigLoader

agent_config_dict = {
    "name": "Assistant",
    "system_message": "You are a helpful AI assistant.",
    "human_input_mode": "NEVER"
}

agent_config = ConfigLoader.load_from_dict(agent_config_dict, "autogen_agent")
```

### Loading from a JSON String

```python
json_string = '''
{
    "model": "gpt-4",
    "api_key": "${OPENAI_API_KEY}",
    "api_type": "openai"
}
'''

llm_config = ConfigLoader.load_from_json_string(json_string, "llm")
```

### Loading from a File

```python
config_path = "path/to/config.json"
config = ConfigLoader.load_from_file(config_path, "autogen_agent")
```

### Loading a Complete Autogen Configuration

```python
config_path = "path/to/autogen_config.json"
autogen_config = ConfigLoader.load_autogen_config(config_path)

# Access agents, group chats, and tools
agents = autogen_config["agents"]
group_chats = autogen_config["group_chats"]
tools = autogen_config["tools"]
```

## Environment Variable Substitution

The `ConfigLoader` supports environment variable substitution in configuration values. Environment variables are specified using the `${VAR_NAME}` syntax:

```json
{
  "model": "gpt-4",
  "api_key": "${OPENAI_API_KEY}",
  "api_type": "openai"
}
```

When the configuration is loaded, `${OPENAI_API_KEY}` will be replaced with the value of the `OPENAI_API_KEY` environment variable.

## Error Handling

The `ConfigLoader` provides two types of exceptions for error handling:

- `ConfigLoadError`: Raised when a configuration cannot be loaded (e.g., file not found, invalid JSON)
- `ConfigValidationError`: Raised when a configuration fails validation (e.g., missing required fields)

Example:

```python
from vaahai.agents.config_loader import ConfigLoader, ConfigLoadError, ConfigValidationError

try:
    config = ConfigLoader.load_from_file("path/to/config.json", "autogen_agent")
except ConfigLoadError as e:
    print(f"Error loading configuration: {e}")
except ConfigValidationError as e:
    print(f"Configuration validation error: {e}")
```

## Examples

### Complete Autogen Configuration Example

```json
{
  "agents": {
    "assistant": {
      "name": "Assistant",
      "system_message": "You are a helpful AI assistant.",
      "human_input_mode": "NEVER",
      "llm_config": {
        "config_list": [
          {
            "model": "gpt-4",
            "api_key": "${OPENAI_API_KEY}",
            "api_type": "openai"
          }
        ],
        "temperature": 0.7
      }
    },
    "coder": {
      "name": "Coder",
      "system_message": "You are an expert programmer.",
      "human_input_mode": "NEVER",
      "llm_config": {
        "config_list": [
          {
            "model": "gpt-4",
            "api_key": "${OPENAI_API_KEY}",
            "api_type": "openai"
          }
        ],
        "temperature": 0.2
      }
    }
  },
  "group_chats": {
    "coding_chat": {
      "name": "CodingChat",
      "agents": ["assistant", "coder"],
      "max_round": 10
    }
  },
  "tools": {
    "calculator": {
      "name": "Calculator",
      "description": "Performs mathematical calculations",
      "parameters": {
        "expression": {
          "type": "string",
          "description": "Mathematical expression to evaluate"
        }
      }
    }
  }
}
```

### Loading and Using Configurations

```python
import os
from vaahai.agents.config_loader import ConfigLoader

# Set environment variables
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Load the complete Autogen configuration
config_path = "path/to/autogen_config.json"
autogen_config = ConfigLoader.load_autogen_config(config_path)

# Access agent configurations
assistant_config = autogen_config["agents"]["assistant"]
coder_config = autogen_config["agents"]["coder"]

# Access group chat configurations
coding_chat_config = autogen_config["group_chats"]["coding_chat"]

# Access tool configurations
calculator_config = autogen_config["tools"]["calculator"]

# Use the configurations to create Autogen components
# (This part depends on how you integrate with Autogen)
```

For more examples, see the `examples` directory in the VaahAI project:
- `examples/autogen_config_example.json`: Example Autogen configuration file
- `examples/load_autogen_config.py`: Example script for loading Autogen configurations
- `examples/load_config_from_file.py`: Example script demonstrating various ConfigLoader features
