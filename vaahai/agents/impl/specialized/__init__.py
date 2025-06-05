"""
VaahAI Specialized Agent Implementations

This package contains specialized agent implementations for specific tasks,
such as code review, security auditing, language detection, and report generation.
"""

from .base import SpecializedAgent
from .code_review import CodeReviewAgent
from .security_audit import SecurityAuditAgent
from .language_detection import LanguageDetectionAgent
from .report_generation import ReportGenerationAgent

__all__ = [
    'SpecializedAgent',
    'CodeReviewAgent',
    'SecurityAuditAgent',
    'LanguageDetectionAgent',
    'ReportGenerationAgent'
]
