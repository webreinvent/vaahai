"""
Configuration schemas for VaahAI agent architecture.

This module defines JSON schemas for configuring various components of the VaahAI
agent architecture, including Autogen integration. These schemas are used for
validation and documentation of configuration options.
"""

from typing import Dict, Any, List, Optional, Union
from enum import Enum


class ApiType(str, Enum):
    """Enum for API types supported by Autogen."""
    OPENAI = "openai"
    AZURE = "azure"
    CUSTOM = "custom"


# Base schema for all LLM configurations
BASE_LLM_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "model": {
            "type": "string",
            "description": "The identifier of the model to be used"
        },
        "api_key": {
            "type": "string",
            "description": "The API key required for authenticating requests"
        },
        "api_rate_limit": {
            "type": "number",
            "description": "Maximum number of API requests permitted per second",
            "minimum": 0
        },
        "base_url": {
            "type": "string",
            "description": "The base URL of the API endpoint"
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Tags which can be used for filtering"
        }
    },
    "required": ["model"]
}

# OpenAI specific configuration schema
OPENAI_CONFIG_SCHEMA = {
    **BASE_LLM_CONFIG_SCHEMA,
    "properties": {
        **BASE_LLM_CONFIG_SCHEMA["properties"],
        "api_type": {
            "type": "string",
            "enum": ["openai"],
            "description": "API type, must be 'openai' for OpenAI configuration"
        },
        "organization": {
            "type": "string",
            "description": "The organization ID for OpenAI"
        }
    },
    "required": ["model", "api_type"]
}

# Azure OpenAI specific configuration schema
AZURE_OPENAI_CONFIG_SCHEMA = {
    **BASE_LLM_CONFIG_SCHEMA,
    "properties": {
        **BASE_LLM_CONFIG_SCHEMA["properties"],
        "api_type": {
            "type": "string",
            "enum": ["azure"],
            "description": "API type, must be 'azure' for Azure OpenAI configuration"
        },
        "api_version": {
            "type": "string",
            "description": "The version of the Azure API to use"
        }
    },
    "required": ["model", "api_type", "base_url"]
}

# Custom LLM configuration schema (for OpenAI-compatible APIs)
CUSTOM_LLM_CONFIG_SCHEMA = {
    **BASE_LLM_CONFIG_SCHEMA,
    "properties": {
        **BASE_LLM_CONFIG_SCHEMA["properties"],
        "api_type": {
            "type": "string",
            "enum": ["custom"],
            "description": "API type, must be 'custom' for custom LLM configuration"
        }
    },
    "required": ["model", "base_url"]
}

# Schema for config_list
CONFIG_LIST_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "model": {
                "type": "string",
                "description": "The identifier of the model to be used"
            },
            "api_key": {
                "type": "string",
                "description": "The API key required for authenticating requests"
            }
        },
        "required": ["model"]
    },
    "description": "List of LLM configurations to use"
}

# Schema for AutoGen-specific parameters
AUTOGEN_PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "cache_seed": {
            "type": ["integer", "null"],
            "description": "Seed for caching. Set to None to disable caching."
        },
        "temperature": {
            "type": "number",
            "description": "Sampling temperature to use",
            "minimum": 0,
            "maximum": 2
        },
        "max_tokens": {
            "type": "integer",
            "description": "Maximum number of tokens to generate",
            "minimum": 1
        },
        "top_p": {
            "type": "number",
            "description": "Nucleus sampling parameter",
            "minimum": 0,
            "maximum": 1
        },
        "timeout": {
            "type": "number",
            "description": "Timeout for API requests in seconds",
            "minimum": 0
        },
        "request_timeout": {
            "type": "number",
            "description": "Timeout for individual requests in seconds",
            "minimum": 0
        }
    }
}

# Schema for Autogen agent configuration
AUTOGEN_AGENT_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the agent"
        },
        "system_message": {
            "type": "string",
            "description": "System message for the agent"
        },
        "llm_config": {
            "type": "object",
            "properties": {
                "config_list": CONFIG_LIST_SCHEMA
            }
        },
        "human_input_mode": {
            "type": "string",
            "enum": ["ALWAYS", "NEVER", "TERMINATE"],
            "description": "When to request human input"
        },
        "max_consecutive_auto_reply": {
            "type": "integer",
            "description": "Maximum number of consecutive auto-replies",
            "minimum": 0
        },
        "is_termination_msg": {
            "type": "boolean",
            "description": "Whether this message should terminate the conversation"
        },
        "code_execution_config": {
            "type": "object",
            "properties": {
                "work_dir": {
                    "type": "string",
                    "description": "Working directory for code execution"
                },
                "use_docker": {
                    "type": ["string", "boolean"],
                    "description": "Whether to use Docker for code execution"
                }
            }
        }
    },
    "required": ["name"]
}

# Schema for Autogen group chat configuration
AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the group chat"
        },
        "agents": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "List of agent names to include in the group chat"
        },
        "messages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Content of the message"
                    },
                    "role": {
                        "type": "string",
                        "description": "Role of the message sender"
                    }
                },
                "required": ["content", "role"]
            },
            "description": "Initial messages for the group chat"
        },
        "max_round": {
            "type": "integer",
            "description": "Maximum number of rounds in the group chat",
            "minimum": 1
        },
        "speaker_selection_method": {
            "type": "string",
            "enum": ["auto", "round_robin", "random", "manual"],
            "description": "Method for selecting the next speaker"
        },
        "allow_repeat_speaker": {
            "type": "boolean",
            "description": "Whether to allow the same speaker multiple times in a row"
        }
    },
    "required": ["name", "agents"]
}

# Schema for Autogen tool configuration
AUTOGEN_TOOL_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the tool"
        },
        "description": {
            "type": "string",
            "description": "Description of what the tool does"
        },
        "parameters": {
            "type": "object",
            "description": "Parameters for the tool"
        },
        "return_direct": {
            "type": "boolean",
            "description": "Whether to return the result directly"
        }
    },
    "required": ["name", "description"]
}

# Complete Autogen configuration schema
AUTOGEN_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "agents": {
            "type": "object",
            "additionalProperties": AUTOGEN_AGENT_CONFIG_SCHEMA,
            "description": "Configuration for agents"
        },
        "group_chats": {
            "type": "object",
            "additionalProperties": AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA,
            "description": "Configuration for group chats"
        },
        "tools": {
            "type": "object",
            "additionalProperties": AUTOGEN_TOOL_CONFIG_SCHEMA,
            "description": "Configuration for tools"
        }
    }
}


def get_schema_for_config_type(config_type: str) -> Dict[str, Any]:
    """
    Get the schema for a specific configuration type.
    
    Args:
        config_type: Type of configuration schema to retrieve
        
    Returns:
        JSON schema for the specified configuration type
        
    Raises:
        ValueError: If the config_type is not supported
    """
    schema_map = {
        "agent": AUTOGEN_AGENT_CONFIG_SCHEMA,
        "group_chat": AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA,
        "tool": AUTOGEN_TOOL_CONFIG_SCHEMA,
        "llm": BASE_LLM_CONFIG_SCHEMA,
        "openai": OPENAI_CONFIG_SCHEMA,
        "azure": AZURE_OPENAI_CONFIG_SCHEMA,
        "custom": CUSTOM_LLM_CONFIG_SCHEMA,
        "config_list": CONFIG_LIST_SCHEMA,
        "autogen": AUTOGEN_CONFIG_SCHEMA
    }
    
    if config_type not in schema_map:
        raise ValueError(f"Unsupported config type: {config_type}. "
                         f"Supported types: {list(schema_map.keys())}")
    
    return schema_map[config_type]
