"""
VaahAI Code Review Agent Implementation

This module provides the CodeReviewAgent class, which specializes in
code quality assessment and improvement suggestions.
"""

import logging
from typing import Dict, Any, List, Optional

from ...exceptions import (
    AgentConfigurationError,
    AgentCommunicationError,
    CodeReviewError,
    AgentMessageError
)
from .base import SpecializedAgent

logger = logging.getLogger(__name__)


class CodeReviewAgent(SpecializedAgent):
    """
    A specialized agent for code review.
    
    CodeReviewAgent extends SpecializedAgent with capabilities specific to
    code review, such as code quality assessment, style checking, and
    improvement suggestions.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new code review agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name or "CodeReviewer")
        self._languages: List[str] = []
        self._review_criteria: List[str] = []
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the agent with the provided configuration.
        
        Args:
            config: Configuration dictionary for the agent
            
        Returns:
            True if initialization was successful, False otherwise
        """
        # Update the agent name if provided in the config
        if 'name' in config and isinstance(config['name'], str):
            self._name = config['name']
        
        # Continue with normal initialization
        return super().initialize(config)
    
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
            
        Raises:
            AgentConfigurationError: If the configuration is invalid
        """
        # First validate using parent class validation
        try:
            if not super()._validate_config():
                return False
        except Exception as e:
            # Re-raise with more context
            raise AgentConfigurationError(self._name, "base_config", str(e))
        
        # Validate languages if provided
        if 'languages' in self._config:
            if not isinstance(self._config['languages'], list):
                error_msg = "languages must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "languages", error_msg)
            
            for lang in self._config['languages']:
                if not isinstance(lang, str):
                    error_msg = "each language must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "languages", error_msg)
            
            self._languages = self._config['languages']
        else:
            logger.warning(f"No languages specified for {self._name}, using empty list")
            self._languages = []
        
        # Validate review criteria if provided
        if 'review_criteria' in self._config:
            if not isinstance(self._config['review_criteria'], list):
                error_msg = "review_criteria must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "review_criteria", error_msg)
            
            for criterion in self._config['review_criteria']:
                if not isinstance(criterion, str):
                    error_msg = "each review criterion must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "review_criteria", error_msg)
            
            self._review_criteria = self._config['review_criteria']
        else:
            logger.info(f"No review criteria specified for {self._name}, using default criteria")
            self._review_criteria = ["style", "complexity", "performance", "security", "readability", "maintainability"]
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add code review capabilities
        self.add_capability('code_review')
        self.add_capability('code_quality')
        self.add_capability('code_quality_assessment')
        
        # Add language-specific capabilities
        for language in self._languages:
            self.add_capability(f"language_{language}")
            self.add_capability(f"review_{language}")
        
        # Add criteria-specific capabilities
        for criterion in self._review_criteria:
            self.add_capability(f"assess_{criterion}")
    
    def get_supported_languages(self) -> List[str]:
        """
        Get the list of programming languages this agent can review.
        
        Returns:
            List of supported language identifiers
        """
        return self._languages
    
    def get_review_criteria(self) -> List[str]:
        """
        Get the list of review criteria this agent evaluates.
        
        Returns:
            List of review criterion identifiers
        """
        return self._review_criteria
    
    def _detect_language(self, code: str) -> str:
        """
        Detect the programming language of the given code.
        
        This is a simplified implementation that uses basic heuristics.
        A real implementation would use more sophisticated techniques.
        
        Args:
            code: The code to analyze
            
        Returns:
            Detected language identifier, or "unknown" if detection fails
        """
        # Simple language detection based on keywords and syntax patterns
        code = code.strip()
        
        # Python detection - improved to catch more Python patterns
        if (("def " in code and ":" in code) or 
            ("import " in code) or 
            ("class " in code and ":" in code) or
            ("print(" in code) or
            ("self." in code)):
            return "python"
        
        # JavaScript detection
        elif (("function " in code and "{" in code) or 
              ("const " in code or "let " in code or "var " in code) or
              ("=> {" in code)):
            return "javascript"
        
        # Java detection
        elif (("public class " in code) or 
              ("private " in code) or 
              ("protected " in code) or
              ("import java." in code)):
            return "java"
        
        # HTML detection
        elif ("<html" in code.lower() and "</html>" in code.lower()):
            return "html"
        
        # CSS detection
        elif ("{" in code and "}" in code and ":" in code and ";" in code and 
              any(selector in code for selector in ["#", ".", "body", "div", "@media"])):
            return "css"
        
        # C++ detection
        elif (("#include" in code) or 
              ("int main" in code or "void main" in code) or
              ("namespace " in code) or
              ("std::" in code)):
            return "c++"
        
        # Default to unknown
        return "unknown"
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a code review response for the given message.
        
        Args:
            message: The message containing code to review
            
        Returns:
            Code review response message
            
        Raises:
            AgentMessageError: If the message format is invalid
            CodeReviewError: If there is an error during code review
        """
        try:
            # Validate message format
            if not isinstance(message, dict):
                raise AgentMessageError(self._name, "unknown", "Message must be a dictionary")
            
            message_type = message.get('type', 'unknown')
            
            if 'code' not in message:
                raise AgentMessageError(
                    self._name,
                    message_type,
                    "Message must contain 'code' field for review"
                )
            
            code = message['code']
            if not isinstance(code, str):
                raise AgentMessageError(
                    self._name,
                    message_type,
                    "Code must be a string"
                )
            
            # Detect language if possible (simplified implementation)
            detected_language = self._detect_language(code)
            
            # Check if we support this language
            if detected_language and self._languages and detected_language not in self._languages:
                raise CodeReviewError(
                    self._name,
                    f"Unsupported programming language: {detected_language}",
                    language=detected_language
                )
            
            # In a real implementation, this would analyze the code and provide review comments
            # For now, we return a placeholder response
            code_snippet = code[:30] + "..." if len(code) > 30 else code
            
            return {
                'type': 'code_review',
                'content': f"Code Review Agent {self._name} has reviewed your code: '{code_snippet}'",
                'sender': self._name,
                'recipient': message.get('sender', 'user'),
                'timestamp': self._get_timestamp(),
                'language': detected_language,
                'review_summary': "This is a placeholder code review.",
                'issues': [
                    {
                        'severity': 'medium',
                        'line': 1,
                        'message': "Consider adding docstrings for better documentation.",
                        'suggestion': "Add a docstring explaining the purpose of this code."
                    },
                    {
                        'severity': 'low',
                        'line': 2,
                        'message': "Variable naming could be improved for clarity.",
                        'suggestion': "Use more descriptive variable names."
                    }
                ],
                'suggestions': [
                    "Add proper docstrings to improve code readability.",
                    "Use more descriptive variable names.",
                    "Consider adding type hints for better code maintainability."
                ],
                'criteria_scores': {
                    'complexity': 'low',
                    'maintainability': 'high',
                    'performance': 'medium',
                    'readability': 'medium',
                    'style': 'medium'
                }
            }
        except (AgentMessageError, CodeReviewError) as e:
            # Re-raise specialized exceptions
            logger.error(f"Error in code review: {str(e)}")
            raise
        except Exception as e:
            # Wrap other exceptions
            logger.error(f"Unexpected error generating code review response: {str(e)}")
            raise CodeReviewError(
                self._name,
                f"Failed to generate code review: {str(e)}",
                language=message.get('language', 'unknown')
            )
