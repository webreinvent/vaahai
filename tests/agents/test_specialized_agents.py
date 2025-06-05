"""
Tests for specialized agent implementations.

This module tests the functionality of specialized agents after refactoring
from a single file to a modular directory structure.
"""

import pytest
import asyncio
from typing import Dict, Any

from vaahai.agents.factory import AgentFactory
from vaahai.agents.exceptions import (
    AgentError,
    AgentConfigurationError,
    AgentTypeNotFoundError,
    AgentInitializationError,
    AgentMessageError,
    AgentCapabilityError,
    CodeReviewError,
    SecurityAuditError,
    LanguageDetectionError,
    ReportGenerationError
)
from vaahai.agents.impl.specialized import (
    SpecializedAgent,
    CodeReviewAgent,
    SecurityAuditAgent,
    LanguageDetectionAgent,
    ReportGenerationAgent
)


class TestSpecializedAgents:
    """Test suite for specialized agents."""

    def test_import_structure(self):
        """Test that all specialized agents can be imported correctly."""
        # If imports are broken, this test would fail during setup
        assert SpecializedAgent is not None
        assert CodeReviewAgent is not None
        assert SecurityAuditAgent is not None
        assert LanguageDetectionAgent is not None
        assert ReportGenerationAgent is not None

    def test_agent_factory_registration(self):
        """Test that all specialized agents are registered with the factory."""
        factory = AgentFactory()
        
        # Check that all specialized agent types are registered
        assert factory.get_component("specialized") is not None
        assert factory.get_component("code_review") is not None
        assert factory.get_component("security_audit") is not None
        assert factory.get_component("language_detection") is not None
        assert factory.get_component("report_generation") is not None

    def test_specialized_agent_initialization(self):
        """Test that specialized agents can be initialized with valid config."""
        agent = SpecializedAgent()
        config = {
            "name": "TestSpecializedAgent",
            "type": "specialized",
            "domain": "testing",
            "expertise": ["unit_testing", "integration_testing"]
        }
        agent.initialize(config)
        
        assert agent.get_domain() == "testing"
        assert "unit_testing" in agent.get_expertise()
        assert "integration_testing" in agent.get_expertise()

    def test_code_review_agent_initialization(self):
        """Test that code review agent can be initialized with valid config."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestCodeReviewAgent",
            "type": "code_review",
            "domain": "code_quality",
            "expertise": ["python", "best_practices"],
            "languages": ["python", "javascript"],
            "review_criteria": ["readability", "maintainability"]
        }
        agent.initialize(config)
        
        assert agent.get_domain() == "code_quality"
        assert "python" in agent.get_supported_languages()
        assert "javascript" in agent.get_supported_languages()
        assert "readability" in agent.get_review_criteria()

    def test_code_review_agent_default_criteria(self):
        """Test that code review agent uses default criteria when not specified."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestCodeReviewAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["python"]
        }
        agent.initialize(config)
        
        # Check that default criteria are used
        criteria = agent.get_review_criteria()
        assert len(criteria) > 0
        assert "readability" in criteria
        assert "maintainability" in criteria

    def test_security_audit_agent_initialization(self):
        """Test that security audit agent can be initialized with valid config."""
        agent = SecurityAuditAgent()
        config = {
            "name": "TestSecurityAuditAgent",
            "type": "security_audit",
            "domain": "security",
            "expertise": ["vulnerability_assessment", "penetration_testing"],
            "compliance_standards": ["OWASP", "PCI-DSS"],
            "vulnerability_categories": ["injection", "xss", "csrf"]
        }
        agent.initialize(config)
        
        assert agent.get_domain() == "security"
        assert "OWASP" in agent.get_compliance_standards()
        assert "injection" in agent.get_vulnerability_categories()

    def test_language_detection_agent_initialization(self):
        """Test that language detection agent can be initialized with valid config."""
        agent = LanguageDetectionAgent()
        config = {
            "name": "TestLanguageDetectionAgent",
            "type": "language_detection",
            "domain": "code_analysis",
            "expertise": ["language_detection", "syntax_analysis"],
            "detectable_languages": ["python", "javascript", "java", "c++"]
        }
        agent.initialize(config)
        
        assert agent.get_domain() == "code_analysis"
        assert "python" in agent.get_detectable_languages()
        assert "c++" in agent.get_detectable_languages()

    def test_report_generation_agent_initialization(self):
        """Test that report generation agent can be initialized with valid config."""
        agent = ReportGenerationAgent()
        config = {
            "name": "TestReportGenerationAgent",
            "type": "report_generation",
            "domain": "reporting",
            "expertise": ["data_visualization", "technical_writing"],
            "report_formats": ["markdown", "html", "pdf"],
            "visualization_types": ["bar_chart", "line_graph", "pie_chart"]
        }
        agent.initialize(config)
        
        assert agent.get_domain() == "reporting"
        assert "markdown" in agent.get_supported_formats()
        assert "bar_chart" in agent.get_visualization_types()

    def test_invalid_config_raises_exception(self):
        """Test that invalid configuration raises AgentConfigurationError."""
        agent = CodeReviewAgent()
        invalid_config = {
            "name": "TestInvalidAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": "python"  # Should be a list, not a string
        }
        
        with pytest.raises(AgentConfigurationError) as excinfo:
            agent.initialize(invalid_config)
        
        assert "languages must be a list" in str(excinfo.value)
        assert "TestInvalidAgent" in str(excinfo.value)
        assert excinfo.value.field == "languages"

    def test_factory_creates_specialized_agents(self):
        """Test that the factory can create specialized agents."""
        factory = AgentFactory()
        
        # Test creating a code review agent
        config = {
            "name": "TestFactoryCodeReviewAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["python", "javascript"]
        }
        agent = factory.create_agent("code_review", config)
        
        assert isinstance(agent, CodeReviewAgent)
        assert "python" in agent.get_supported_languages()

    def test_factory_invalid_agent_type(self):
        """Test that the factory raises AgentTypeNotFoundError for invalid agent types."""
        factory = AgentFactory()
        
        with pytest.raises(AgentTypeNotFoundError) as excinfo:
            factory.create_agent("NonExistentAgent", {})
        
        assert "NonExistentAgent" in str(excinfo.value)
        assert excinfo.value.agent_type == "NonExistentAgent"

    def test_factory_initialization_error(self):
        """Test that the factory wraps initialization errors in AgentInitializationError."""
        factory = AgentFactory()
        
        invalid_config = {
            "name": "TestInvalidTypeAgent",
            "type": "code_review",
            "domain": 123  # Should be a string, not an integer
        }
        
        with pytest.raises(AgentInitializationError) as excinfo:
            factory.create_agent("code_review", invalid_config)
        
        assert "code_review" in str(excinfo.value)
        assert excinfo.value.agent_name == "TestInvalidTypeAgent"

    @pytest.mark.asyncio
    async def test_code_review_agent_response(self):
        """Test that code review agent can generate responses."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestCodeReviewResponseAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["python"]
        }
        agent.initialize(config)
        
        message = {
            "type": "text",
            "content": "Please review this code",
            "sender": "user",
            "code": "def add(a, b):\n    return a + b"
        }
        
        response = await agent._generate_response(message)
        
        assert response["type"] == "code_review"
        assert "sender" in response
        assert "review_summary" in response
        assert "suggestions" in response
        assert "criteria_scores" in response
        assert response["language"] == "python"

    @pytest.mark.asyncio
    async def test_code_review_agent_missing_code_error(self):
        """Test that code review agent raises error when code is missing."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestCodeReviewErrorAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["python"]
        }
        agent.initialize(config)
        
        message = {
            "type": "text",
            "content": "Please review this code",
            "sender": "user"
            # Missing 'code' field
        }
        
        with pytest.raises(AgentMessageError) as excinfo:
            await agent._generate_response(message)
        
        assert "code" in str(excinfo.value)
        assert excinfo.value.agent_name == "TestCodeReviewErrorAgent"
        assert excinfo.value.message_type == "text"

    @pytest.mark.asyncio
    async def test_code_review_agent_unsupported_language(self):
        """Test that code review agent raises error for unsupported languages."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestCodeReviewLangAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["javascript"]  # Only supports JavaScript
        }
        agent.initialize(config)
        
        # Python code
        message = {
            "type": "text",
            "content": "Please review this code",
            "sender": "user",
            "code": "def add(a, b):\n    return a + b"  # Python code
        }
        
        with pytest.raises(CodeReviewError) as excinfo:
            await agent._generate_response(message)
        
        assert "Unsupported programming language" in str(excinfo.value)
        assert excinfo.value.language == "python"
        assert excinfo.value.agent_name == "TestCodeReviewLangAgent"

    @pytest.mark.asyncio
    async def test_code_review_language_detection(self):
        """Test that code review agent correctly detects languages."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestLangDetectionAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["python", "javascript", "java", "html"]
        }
        agent.initialize(config)
        
        # Test Python detection
        python_message = {
            "type": "text",
            "sender": "user",
            "code": "def hello():\n    print('Hello, world!')"
        }
        python_response = await agent._generate_response(python_message)
        assert python_response["language"] == "python"
        
        # Test JavaScript detection
        js_message = {
            "type": "text",
            "sender": "user",
            "code": "function hello() {\n    console.log('Hello, world!');\n}"
        }
        js_response = await agent._generate_response(js_message)
        assert js_response["language"] == "javascript"
        
        # Test HTML detection
        html_message = {
            "type": "text",
            "sender": "user",
            "code": "<html><body><h1>Hello, world!</h1></body></html>"
        }
        html_response = await agent._generate_response(html_message)
        assert html_response["language"] == "html"

    @pytest.mark.asyncio
    async def test_security_audit_agent_response(self):
        """Test that security audit agent can generate responses."""
        agent = SecurityAuditAgent()
        config = {
            "name": "TestSecurityAuditResponseAgent",
            "type": "security_audit",
            "domain": "security",
            "compliance_standards": ["OWASP"]
        }
        agent.initialize(config)
        
        message = {
            "type": "text",
            "content": "Please audit this code",
            "sender": "user",
            "code": "password = 'hardcoded'"
        }
        
        response = await agent._generate_response(message)
        
        assert response["type"] == "security_audit"
        assert "sender" in response
        assert "audit_summary" in response
        assert "findings" in response

    @pytest.mark.asyncio
    async def test_language_detection_agent_response(self):
        """Test that language detection agent can generate responses."""
        agent = LanguageDetectionAgent()
        config = {
            "name": "TestLanguageDetectionResponseAgent",
            "type": "language_detection",
            "domain": "code_analysis",
            "detectable_languages": ["python", "javascript"]
        }
        agent.initialize(config)
        
        message = {
            "type": "text",
            "content": "What language is this?",
            "sender": "user",
            "code": "def hello():\n    print('Hello, world!')"
        }
        
        response = await agent._generate_response(message)
        
        assert response["type"] == "language_detection"
        assert "sender" in response
        assert "detected_language" in response
        assert "confidence" in response

    @pytest.mark.asyncio
    async def test_report_generation_agent_response(self):
        """Test that report generation agent can generate responses."""
        agent = ReportGenerationAgent()
        config = {
            "name": "TestReportGenerationResponseAgent",
            "type": "report_generation",
            "domain": "reporting",
            "report_formats": ["markdown", "html"]
        }
        agent.initialize(config)
        
        message = {
            "type": "text",
            "content": "Generate a report",
            "sender": "user",
            "data": {"key": "value"},
            "format": "markdown",
            "title": "Test Report"
        }
        
        response = await agent._generate_response(message)
        
        assert response["type"] == "report"
        assert "sender" in response
        assert "report_format" in response
        assert response["report_format"] == "markdown"
        assert "report_content" in response
        assert "Test Report" in response["report_content"]

    def test_agent_capability_validation(self):
        """Test that agents correctly validate their capabilities."""
        agent = CodeReviewAgent()
        config = {
            "name": "TestCapabilityAgent",
            "type": "code_review",
            "domain": "code_quality",
            "languages": ["python"]
        }
        agent.initialize(config)
        
        # Should have these capabilities
        assert agent.has_capability("code_quality_assessment")
        assert agent.has_capability("language_python")
        
        # Should not have these capabilities
        assert not agent.has_capability("language_javascript")
        assert not agent.has_capability("security_audit")


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
