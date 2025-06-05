"""
Group Chat Configuration Classes

This module provides configuration classes for group chats, including basic group chat
configuration and Autogen-specific group chat configuration.
"""

from typing import Dict, Any, List, Optional, Union, Set

from .base import BaseConfig
from ..schemas import AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA


class GroupChatConfig(BaseConfig):
    """
    Configuration for group chats.
    
    This class provides structured configuration for group chats, with validation
    to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new group chat configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"type"}
        self._optional_fields = {
            "name": "GroupChat",
            "agents": [],
            "max_rounds": 10,
            "termination_conditions": [],
            "selector": None,
            "human_input_mode": "NEVER",
            "metadata": {}
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
    
    def _validate_field(self, field: str, value: Any) -> bool:
        """
        Validate a configuration field.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if the field is valid, False otherwise
        """
        if field == "type":
            return isinstance(value, str) and len(value) > 0
        elif field == "name":
            return isinstance(value, str) and len(value) > 0
        elif field == "agents":
            return isinstance(value, list)
        elif field == "max_rounds":
            return isinstance(value, int) and value > 0
        elif field == "termination_conditions":
            return isinstance(value, list)
        elif field == "selector":
            return value is None or isinstance(value, dict)
        elif field == "human_input_mode":
            return isinstance(value, str) and value in ["NEVER", "TERMINATE", "ALWAYS"]
        elif field == "metadata":
            return isinstance(value, dict)
        return True


class AutogenGroupChatConfig(BaseConfig):
    """
    Configuration for Autogen group chats.
    
    This class provides structured configuration for Autogen group chats, with validation
    using JSON schema to ensure that required fields are present and have valid values.
    """
    
    def __init__(self, **kwargs):
        """
        Initialize a new Autogen group chat configuration.
        
        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._required_fields = {"name", "agents"}
        self._optional_fields = {
            "messages": [],
            "max_round": 10,
            "speaker_selection_method": "auto",
            "allow_repeat_speaker": False,
            "metadata": {}
        }
        
        # Set default values for optional fields
        for field, default in self._optional_fields.items():
            if field not in self._config:
                self._config[field] = default
        
        # Set schema
        self._schema = AUTOGEN_GROUP_CHAT_CONFIG_SCHEMA
    
    def _validate_field(self, field: str, value: Any) -> bool:
        """
        Validate a configuration field.
        
        Args:
            field: Field name
            value: Field value
            
        Returns:
            True if the field is valid, False otherwise
        """
        if field == "name":
            return isinstance(value, str) and len(value) > 0
        elif field == "agents":
            return isinstance(value, list) and len(value) > 0
        elif field == "messages":
            return isinstance(value, list)
        elif field == "max_round":
            return isinstance(value, int) and value > 0
        elif field == "speaker_selection_method":
            return isinstance(value, str) and value in ["auto", "round_robin", "random"]
        elif field == "allow_repeat_speaker":
            return isinstance(value, bool)
        elif field == "metadata":
            return isinstance(value, dict)
        return True
