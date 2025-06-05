"""
Schema validation utilities for agent configurations.

This module provides functions for validating agent configurations against
JSON schemas defined in the schemas module.
"""

import logging
import jsonschema
from typing import Dict, Any, Optional, List, Tuple

from .schemas import get_schema_for_config_type
from .exceptions import AgentConfigurationError

logger = logging.getLogger(__name__)


def validate_agent_config(config: Dict[str, Any], agent_type: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an agent configuration against its schema.
    
    Args:
        config: The configuration to validate
        agent_type: The type of agent to validate against
        
    Returns:
        A tuple of (is_valid, error_message)
    """
    try:
        # Determine the schema type based on agent_type
        schema_type = _get_schema_type_for_agent(agent_type)
        
        # Get the schema
        schema = get_schema_for_config_type(schema_type)
        
        # Validate the configuration against the schema
        jsonschema.validate(instance=config, schema=schema)
        
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        # Extract the most useful parts of the validation error
        error_path = ".".join(str(path) for path in e.path) if e.path else "root"
        error_message = f"Validation error at {error_path}: {e.message}"
        logger.error(f"Configuration validation failed: {error_message}")
        return False, error_message
    except ValueError as e:
        # This happens if the schema type is not supported
        logger.error(f"Schema validation error: {str(e)}")
        return False, str(e)
    except Exception as e:
        # Catch any other exceptions
        logger.error(f"Unexpected error during schema validation: {str(e)}")
        return False, f"Unexpected error: {str(e)}"


def _get_schema_type_for_agent(agent_type: str) -> str:
    """
    Map an agent type to its corresponding schema type.
    
    Args:
        agent_type: The agent type
        
    Returns:
        The schema type to use for validation
        
    Raises:
        ValueError: If the agent type is not supported
    """
    # Map of agent types to schema types
    agent_schema_map = {
        "base": "agent",
        "conversational": "agent",
        "assistant": "agent",
        "user_proxy": "agent",
        "specialized": "specialized_agent",
        "code_review": "code_review_agent",
        "security_audit": "security_audit_agent",
        "language_detection": "language_detection_agent",
        "report_generation": "report_generation_agent"
    }
    
    # Get the schema type, defaulting to "agent" if not found
    schema_type = agent_schema_map.get(agent_type.lower(), None)
    
    if schema_type is None:
        # Check if it's a specialized agent by name
        if "code_review" in agent_type.lower():
            return "code_review_agent"
        elif "security" in agent_type.lower():
            return "security_audit_agent"
        elif "language" in agent_type.lower():
            return "language_detection_agent"
        elif "report" in agent_type.lower():
            return "report_generation_agent"
        elif "specialized" in agent_type.lower():
            return "specialized_agent"
        else:
            # Default to base agent schema
            return "agent"
    
    return schema_type


def get_validation_errors(config: Dict[str, Any], agent_type: str) -> List[str]:
    """
    Get a list of all validation errors for an agent configuration.
    
    Args:
        config: The configuration to validate
        agent_type: The type of agent to validate against
        
    Returns:
        A list of validation error messages
    """
    errors = []
    
    try:
        # Determine the schema type based on agent_type
        schema_type = _get_schema_type_for_agent(agent_type)
        
        # Get the schema
        schema = get_schema_for_config_type(schema_type)
        
        # Create a validator
        validator = jsonschema.Draft7Validator(schema)
        
        # Collect all errors
        for error in validator.iter_errors(config):
            error_path = ".".join(str(path) for path in error.path) if error.path else "root"
            errors.append(f"{error_path}: {error.message}")
    except Exception as e:
        errors.append(f"Schema validation error: {str(e)}")
    
    return errors
