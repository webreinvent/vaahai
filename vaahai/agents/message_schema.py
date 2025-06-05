"""
VaahAI Message Schemas

This module defines JSON schemas for validating agent messages in the VaahAI system.
These schemas ensure that messages exchanged between agents follow a consistent
structure and contain all required fields.
"""

import json
from typing import Dict, Any, Tuple, Optional

# Base message schema that all messages must follow
BASE_MESSAGE_SCHEMA = {
    "type": "object",
    "required": ["message_id", "sender_id", "receiver_id", "content", "timestamp", "message_type"],
    "properties": {
        "message_id": {
            "type": "string",
            "description": "Unique identifier for the message"
        },
        "sender_id": {
            "type": "string",
            "description": "Identifier for the sender"
        },
        "receiver_id": {
            "type": ["string", "null"],
            "description": "Identifier for the receiver, null for broadcast"
        },
        "content": {
            "type": "object",
            "description": "Message content, structure depends on message_type"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp for when the message was created"
        },
        "message_type": {
            "type": "string",
            "enum": ["text", "function_call", "function_result", "error", "system"],
            "description": "Type of message"
        },
        "conversation_id": {
            "type": "string",
            "description": "Identifier for the conversation this message belongs to"
        },
        "in_reply_to": {
            "type": ["string", "null"],
            "description": "Identifier for the message this is a reply to"
        },
        "metadata": {
            "type": "object",
            "description": "Additional metadata for the message",
            "additionalProperties": True
        }
    },
    "additionalProperties": True
}

# Text message schema
TEXT_MESSAGE_SCHEMA = {
    "type": "object",
    "required": ["text"],
    "properties": {
        "text": {
            "type": "string",
            "description": "Text content of the message"
        },
        "format": {
            "type": "string",
            "enum": ["plain", "markdown", "html"],
            "default": "plain",
            "description": "Format of the text content"
        }
    },
    "additionalProperties": True
}

# Function call message schema
FUNCTION_CALL_SCHEMA = {
    "type": "object",
    "required": ["name", "arguments"],
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the function to call"
        },
        "arguments": {
            "type": "object",
            "description": "Arguments to pass to the function"
        },
        "description": {
            "type": "string",
            "description": "Description of the function call"
        }
    },
    "additionalProperties": True
}

# Function result message schema
FUNCTION_RESULT_SCHEMA = {
    "type": "object",
    "required": ["name", "result"],
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the function that was called"
        },
        "result": {
            "type": ["object", "string", "number", "boolean", "array", "null"],
            "description": "Result of the function call"
        }
    },
    "additionalProperties": True
}

# Error message schema
ERROR_MESSAGE_SCHEMA = {
    "type": "object",
    "required": ["error_type", "error_message"],
    "properties": {
        "error_type": {
            "type": "string",
            "description": "Type of error"
        },
        "error_message": {
            "type": "string",
            "description": "Error message"
        },
        "traceback": {
            "type": "string",
            "description": "Error traceback"
        }
    },
    "additionalProperties": True
}

# System message schema
SYSTEM_MESSAGE_SCHEMA = {
    "type": "object",
    "required": ["system_message_type", "system_message"],
    "properties": {
        "system_message_type": {
            "type": "string",
            "enum": ["info", "warning", "error", "debug"],
            "description": "Type of system message"
        },
        "system_message": {
            "type": "string",
            "description": "System message content"
        }
    },
    "additionalProperties": True
}

# Map of message types to their content schemas
MESSAGE_CONTENT_SCHEMAS = {
    "text": TEXT_MESSAGE_SCHEMA,
    "function_call": FUNCTION_CALL_SCHEMA,
    "function_result": FUNCTION_RESULT_SCHEMA,
    "error": ERROR_MESSAGE_SCHEMA,
    "system": SYSTEM_MESSAGE_SCHEMA
}

def get_message_schema(message_type: str) -> Dict[str, Any]:
    """
    Get the schema for a specific message type.
    
    Args:
        message_type: Type of message
        
    Returns:
        JSON schema for the message type
        
    Raises:
        ValueError: If the message type is not supported
    """
    if message_type not in MESSAGE_CONTENT_SCHEMAS:
        raise ValueError(f"Unsupported message type: {message_type}")
    
    return MESSAGE_CONTENT_SCHEMAS[message_type]
