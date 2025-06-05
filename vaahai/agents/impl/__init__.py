"""
VaahAI Agent Implementations

This package contains concrete implementations of the agent interfaces
defined in the interfaces module, building on the base classes from the
base module.
"""

from .conversational import ConversationalAgent
from .assistant import AssistantAgent
from .user_proxy import UserProxyAgent
from .specialized.base import SpecializedAgent
from .specialized.code_review import CodeReviewAgent
from .specialized.security_audit import SecurityAuditAgent
from .specialized.language_detection import LanguageDetectionAgent
from .specialized.report_generation import ReportGenerationAgent

__all__ = [
    'ConversationalAgent',
    'AssistantAgent',
    'UserProxyAgent',
    'SpecializedAgent',
    'CodeReviewAgent',
    'SecurityAuditAgent',
    'LanguageDetectionAgent',
    'ReportGenerationAgent'
]
