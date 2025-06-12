"""
Unit tests for the group chat configuration schema.
"""

import unittest
from vaahai.config.schemas.group_chat import (
    GROUP_CHAT_SCHEMA,
    DEFAULT_GROUP_CHAT_CONFIG,
    GROUP_CHAT_TYPE_SCHEMAS,
    validate_group_chat_config
)


class TestGroupChatSchema(unittest.TestCase):
    """Test cases for the group chat configuration schema."""

    def test_default_config_valid(self):
        """Test that the default configuration is valid."""
        try:
            result = validate_group_chat_config(DEFAULT_GROUP_CHAT_CONFIG)
            self.assertEqual(result["type"], "round_robin")
            self.assertEqual(result["human_input_mode"], "terminate")
            self.assertEqual(result["max_rounds"], 10)
        except ValueError:
            self.fail("Default configuration should be valid")

    def test_round_robin_config(self):
        """Test validation of a round robin configuration."""
        config = {
            "type": "round_robin",
            "human_input_mode": "never",
            "max_rounds": 5
        }
        result = validate_group_chat_config(config)
        self.assertEqual(result["type"], "round_robin")
        self.assertEqual(result["human_input_mode"], "never")
        self.assertEqual(result["max_rounds"], 5)
        # Default values should be preserved
        self.assertEqual(result["allow_repeat_speaker"], False)
        self.assertEqual(result["send_introductions"], True)

    def test_selector_config(self):
        """Test validation of a selector configuration."""
        config = {
            "type": "selector",
            "selector_agent": "coordinator",
            "human_input_mode": "always"
        }
        result = validate_group_chat_config(config)
        self.assertEqual(result["type"], "selector")
        self.assertEqual(result["selector_agent"], "coordinator")
        self.assertEqual(result["human_input_mode"], "always")

    def test_broadcast_config(self):
        """Test validation of a broadcast configuration."""
        config = {
            "type": "broadcast",
            "human_input_mode": "feedback",
            "termination": {
                "max_messages": 20,
                "completion_indicators": ["Done", "Complete"]
            }
        }
        result = validate_group_chat_config(config)
        self.assertEqual(result["type"], "broadcast")
        self.assertEqual(result["human_input_mode"], "feedback")
        self.assertEqual(result["termination"]["max_messages"], 20)
        self.assertEqual(len(result["termination"]["completion_indicators"]), 2)

    def test_custom_config(self):
        """Test validation of a custom configuration."""
        config = {
            "type": "custom",
            "custom_class": "vaahai.agents.utils.custom_chat.MyCustomChat",
            "human_input_mode": "terminate"
        }
        result = validate_group_chat_config(config)
        self.assertEqual(result["type"], "custom")
        self.assertEqual(result["custom_class"], "vaahai.agents.utils.custom_chat.MyCustomChat")

    def test_invalid_chat_type(self):
        """Test validation with an invalid chat type."""
        config = {
            "type": "invalid_type",
            "human_input_mode": "terminate"
        }
        with self.assertRaises(ValueError):
            validate_group_chat_config(config)


if __name__ == "__main__":
    unittest.main()
