"""
VaahAI Agent Exceptions

This module defines custom exceptions used throughout the agent system.
These exceptions provide more specific error information and help with
proper error handling and debugging.
"""

class AgentError(Exception):
    """Base exception class for all agent-related errors."""
    pass


class AgentInitializationError(AgentError):
    """Exception raised when an agent fails to initialize properly."""
    
    def __init__(self, agent_name: str, reason: str):
        self.agent_name = agent_name
        self.reason = reason
        message = f"Failed to initialize agent '{agent_name}': {reason}"
        super().__init__(message)


class AgentConfigurationError(AgentError):
    """Exception raised when an agent's configuration is invalid."""
    
    def __init__(self, agent_name: str, field: str, reason: str):
        self.agent_name = agent_name
        self.field = field
        self.reason = reason
        message = f"Invalid configuration for agent '{agent_name}', field '{field}': {reason}"
        super().__init__(message)


class AgentNotInitializedError(AgentError):
    """Exception raised when attempting to use an uninitialized agent."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        message = f"Agent '{agent_name}' is not initialized"
        super().__init__(message)


class AgentTypeNotFoundError(AgentError):
    """Exception raised when attempting to create an agent of an unregistered type."""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        message = f"Agent type '{agent_type}' is not registered"
        super().__init__(message)


class AgentCapabilityError(AgentError):
    """Exception raised when an agent lacks a required capability."""
    
    def __init__(self, agent_name: str, capability: str):
        self.agent_name = agent_name
        self.capability = capability
        message = f"Agent '{agent_name}' does not have the required capability: {capability}"
        super().__init__(message)


class AgentCommunicationError(AgentError):
    """Exception raised when there's an error in agent communication."""
    
    def __init__(self, agent_name: str, reason: str):
        self.agent_name = agent_name
        self.reason = reason
        message = f"Communication error for agent '{agent_name}': {reason}"
        super().__init__(message)


class AgentToolError(AgentError):
    """Exception raised when there's an error with agent tool usage."""
    
    def __init__(self, agent_name: str, tool_name: str, reason: str):
        self.agent_name = agent_name
        self.tool_name = tool_name
        self.reason = reason
        message = f"Tool error for agent '{agent_name}', tool '{tool_name}': {reason}"
        super().__init__(message)


# Specialized agent exceptions
class SpecializedAgentError(AgentError):
    """Base exception class for specialized agent-related errors."""
    
    def __init__(self, agent_name: str, reason: str):
        self.agent_name = agent_name
        self.reason = reason
        message = f"Specialized agent error for '{agent_name}': {reason}"
        super().__init__(message)


class CodeReviewError(SpecializedAgentError):
    """Exception raised when there's an error in code review operations."""
    
    def __init__(self, agent_name: str, reason: str, language: str = None, file_path: str = None):
        self.language = language
        self.file_path = file_path
        details = []
        if language:
            details.append(f"language: {language}")
        if file_path:
            details.append(f"file: {file_path}")
        
        detail_str = ", ".join(details)
        full_reason = f"{reason} ({detail_str})" if details else reason
        super().__init__(agent_name, full_reason)


class SecurityAuditError(SpecializedAgentError):
    """Exception raised when there's an error in security audit operations."""
    
    def __init__(self, agent_name: str, reason: str, vulnerability_type: str = None, severity: str = None):
        self.vulnerability_type = vulnerability_type
        self.severity = severity
        details = []
        if vulnerability_type:
            details.append(f"vulnerability: {vulnerability_type}")
        if severity:
            details.append(f"severity: {severity}")
        
        detail_str = ", ".join(details)
        full_reason = f"{reason} ({detail_str})" if details else reason
        super().__init__(agent_name, full_reason)


class LanguageDetectionError(SpecializedAgentError):
    """Exception raised when there's an error in language detection operations."""
    
    def __init__(self, agent_name: str, reason: str, content_size: int = None):
        self.content_size = content_size
        detail_str = f"content size: {content_size} bytes" if content_size else ""
        full_reason = f"{reason} ({detail_str})" if detail_str else reason
        super().__init__(agent_name, full_reason)


class ReportGenerationError(SpecializedAgentError):
    """Exception raised when there's an error in report generation operations."""
    
    def __init__(self, agent_name: str, reason: str, report_format: str = None, data_size: int = None):
        self.report_format = report_format
        self.data_size = data_size
        details = []
        if report_format:
            details.append(f"format: {report_format}")
        if data_size:
            details.append(f"data size: {data_size} bytes")
        
        detail_str = ", ".join(details)
        full_reason = f"{reason} ({detail_str})" if details else reason
        super().__init__(agent_name, full_reason)


class AgentMessageError(AgentError):
    """Exception raised when there's an error processing a message."""
    
    def __init__(self, agent_name: str, message_type: str, reason: str):
        self.agent_name = agent_name
        self.message_type = message_type
        self.reason = reason
        message = f"Message error for agent '{agent_name}', message type '{message_type}': {reason}"
        super().__init__(message)


class AgentTimeoutError(AgentError):
    """Exception raised when an agent operation times out."""
    
    def __init__(self, agent_name: str, operation: str, timeout_seconds: float):
        self.agent_name = agent_name
        self.operation = operation
        self.timeout_seconds = timeout_seconds
        message = f"Operation '{operation}' timed out after {timeout_seconds} seconds for agent '{agent_name}'"
        super().__init__(message)


class AgentResourceError(AgentError):
    """Exception raised when an agent encounters resource constraints."""
    
    def __init__(self, agent_name: str, resource_type: str, limit: str, actual: str = None):
        self.agent_name = agent_name
        self.resource_type = resource_type
        self.limit = limit
        self.actual = actual
        detail = f", actual: {actual}" if actual else ""
        message = f"Resource constraint for agent '{agent_name}', {resource_type} limit: {limit}{detail}"
        super().__init__(message)
