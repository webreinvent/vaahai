"""
Tests for agent configuration schema validation.

This module tests the schema validation functionality for agent configurations.
"""

import pytest
from typing import Dict, Any

from vaahai.agents.schema_validator import validate_agent_config, get_validation_errors
from vaahai.agents.factory import AgentFactory
from vaahai.agents.exceptions import AgentInitializationError


class TestAgentSchemas:
    """Tests for agent configuration schema validation."""
    
    def test_base_agent_schema_validation(self):
        """Test validation of base agent schema."""
        # Valid configuration
        valid_config = {
            "name": "test_agent",
            "type": "base"
        }
        is_valid, error = validate_agent_config(valid_config, "base")
        assert is_valid is True
        assert error is None
        
        # Invalid configuration (missing required field)
        invalid_config = {
            "name": "test_agent"
        }
        is_valid, error = validate_agent_config(invalid_config, "base")
        assert is_valid is False
        assert error is not None
        assert "type" in error
        
        # Invalid configuration (wrong type)
        invalid_config = {
            "name": "test_agent",
            "type": "base",
            "max_history_length": "not_an_integer"
        }
        is_valid, error = validate_agent_config(invalid_config, "base")
        assert is_valid is False
        assert error is not None
        assert "max_history_length" in error
    
    def test_specialized_agent_schema_validation(self):
        """Test validation of specialized agent schema."""
        # Valid configuration
        valid_config = {
            "name": "test_specialized_agent",
            "type": "specialized",
            "domain": "testing",
            "expertise": ["unit_testing", "schema_validation"]
        }
        is_valid, error = validate_agent_config(valid_config, "specialized")
        assert is_valid is True
        assert error is None
        
        # Invalid configuration (wrong type for expertise)
        invalid_config = {
            "name": "test_specialized_agent",
            "type": "specialized",
            "domain": "testing",
            "expertise": "not_a_list"
        }
        is_valid, error = validate_agent_config(invalid_config, "specialized")
        assert is_valid is False
        assert error is not None
        assert "expertise" in error
    
    def test_code_review_agent_schema_validation(self):
        """Test validation of code review agent schema."""
        # Valid configuration
        valid_config = {
            "name": "test_code_review_agent",
            "type": "code_review",
            "languages": ["python", "javascript"],
            "review_criteria": ["style", "complexity", "readability"]
        }
        is_valid, error = validate_agent_config(valid_config, "code_review")
        assert is_valid is True
        assert error is None
        
        # Invalid configuration (wrong type for languages)
        invalid_config = {
            "name": "test_code_review_agent",
            "type": "code_review",
            "languages": "python",  # Should be a list
            "review_criteria": ["style", "complexity"]
        }
        is_valid, error = validate_agent_config(invalid_config, "code_review")
        assert is_valid is False
        assert error is not None
        assert "languages" in error
    
    def test_security_audit_agent_schema_validation(self):
        """Test validation of security audit agent schema."""
        # Valid configuration
        valid_config = {
            "name": "test_security_audit_agent",
            "type": "security_audit",
            "vulnerability_types": ["sql_injection", "xss"],
            "severity_levels": ["high", "medium", "low"]
        }
        is_valid, error = validate_agent_config(valid_config, "security_audit")
        assert is_valid is True
        assert error is None
    
    def test_language_detection_agent_schema_validation(self):
        """Test validation of language detection agent schema."""
        # Valid configuration
        valid_config = {
            "name": "test_language_detection_agent",
            "type": "language_detection",
            "supported_languages": ["python", "javascript", "java"],
            "confidence_threshold": 0.8
        }
        is_valid, error = validate_agent_config(valid_config, "language_detection")
        assert is_valid is True
        assert error is None
        
        # Invalid configuration (confidence_threshold out of range)
        invalid_config = {
            "name": "test_language_detection_agent",
            "type": "language_detection",
            "supported_languages": ["python", "javascript"],
            "confidence_threshold": 1.5  # Should be between 0 and 1
        }
        is_valid, error = validate_agent_config(invalid_config, "language_detection")
        assert is_valid is False
        assert error is not None
        assert "confidence_threshold" in error
    
    def test_report_generation_agent_schema_validation(self):
        """Test validation of report generation agent schema."""
        # Valid configuration
        valid_config = {
            "name": "test_report_generation_agent",
            "type": "report_generation",
            "report_formats": ["markdown", "html", "pdf"],
            "templates": {
                "markdown": "# Report Template",
                "html": "<h1>Report Template</h1>"
            }
        }
        is_valid, error = validate_agent_config(valid_config, "report_generation")
        assert is_valid is True
        assert error is None
    
    def test_agent_factory_schema_validation(self):
        """Test that AgentFactory uses schema validation."""
        factory = AgentFactory()
        
        # Valid configuration
        valid_config = {
            "name": "test_agent",
            "type": "conversational"
        }
        
        # Invalid configuration
        invalid_config = {
            "name": "test_agent",
            "type": "conversational",
            "max_history_length": "not_an_integer"  # Should be an integer
        }
        
        # Factory should create agent with valid config
        try:
            factory.create_agent("conversational", valid_config)
        except Exception as e:
            pytest.fail(f"Factory should not raise exception for valid config: {str(e)}")
        
        # Factory should raise exception with invalid config
        with pytest.raises(AgentInitializationError) as excinfo:
            factory.create_agent("conversational", invalid_config)
        
        # Check that the error message contains schema validation details
        assert "Invalid configuration" in str(excinfo.value)
        assert "max_history_length" in str(excinfo.value)
    
    def test_get_validation_errors(self):
        """Test getting all validation errors for a configuration."""
        # Configuration with multiple errors
        invalid_config = {
            "name": 123,  # Should be a string
            "type": "base",
            "max_history_length": "not_an_integer",  # Should be an integer
            "decorators": "not_a_list"  # Should be a list
        }
        
        errors = get_validation_errors(invalid_config, "base")
        
        # Should have at least 3 errors
        assert len(errors) >= 3
        
        # Check that each error is reported
        name_error = any("name" in error for error in errors)
        max_history_error = any("max_history_length" in error for error in errors)
        decorators_error = any("decorators" in error for error in errors)
        
        assert name_error
        assert max_history_error
        assert decorators_error
