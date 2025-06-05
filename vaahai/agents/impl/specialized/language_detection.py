"""
VaahAI Language Detection Agent Implementation

This module provides the LanguageDetectionAgent class, which specializes in
programming language detection and file analysis.
"""

import logging
from typing import Dict, Any, List, Optional

from ...exceptions import AgentConfigurationError, AgentCommunicationError, LanguageDetectionError, AgentMessageError
from .base import SpecializedAgent

logger = logging.getLogger(__name__)


class LanguageDetectionAgent(SpecializedAgent):
    """
    A specialized agent for programming language detection.
    
    LanguageDetectionAgent extends SpecializedAgent with capabilities specific to
    programming language detection, such as file analysis and language identification.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new language detection agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name or "LanguageDetector")
        self._detectable_languages: List[str] = []
    
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
        
        # Validate detectable languages if provided
        if 'detectable_languages' in self._config:
            if not isinstance(self._config['detectable_languages'], list):
                error_msg = "detectable_languages must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "detectable_languages", error_msg)
            
            for lang in self._config['detectable_languages']:
                if not isinstance(lang, str):
                    error_msg = "each detectable language must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "detectable_languages", error_msg)
            
            self._detectable_languages = self._config['detectable_languages']
        else:
            logger.info(f"No detectable languages specified for {self._name}, using default languages")
            self._detectable_languages = ["python", "javascript", "java", "c++", "html", "css"]
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add language detection capabilities
        self.add_capability('language_detection')
        self.add_capability('code_analysis')
        
        # Add language-specific capabilities
        for language in self._detectable_languages:
            self.add_capability(f"detect_{language}")
    
    def get_detectable_languages(self) -> List[str]:
        """
        Get the list of programming languages this agent can detect.
        
        Returns:
            List of detectable language identifiers
        """
        return self._detectable_languages
    
    def _detect_language(self, code: str) -> Dict[str, float]:
        """
        Detect the programming language of the given code.
        
        This is a simplified implementation that uses basic heuristics.
        A real implementation would use more sophisticated techniques.
        
        Args:
            code: The code to analyze
            
        Returns:
            Dictionary mapping language identifiers to confidence scores
        """
        # Simple language detection based on keywords and syntax
        scores = {}
        
        # Python detection
        if "def " in code and ":" in code and ("self" in code or "import " in code):
            scores["python"] = 0.8
        
        # JavaScript detection
        if "function " in code and "{" in code and "}" in code:
            scores["javascript"] = 0.7
        
        # Java detection
        if "public class " in code or "private void " in code:
            scores["java"] = 0.9
        
        # HTML detection
        if "<html" in code.lower() and "</html>" in code.lower():
            scores["html"] = 0.95
        
        # C++ detection
        if "#include" in code and ("int main" in code or "void main" in code):
            scores["c++"] = 0.85
        
        # Default if nothing detected
        if not scores:
            scores["unknown"] = 0.5
        
        return scores
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a language detection response for the given message.
        
        Args:
            message: The message containing code to analyze
            
        Returns:
            Language detection response message
            
        Raises:
            AgentMessageError: If the message format is invalid
            LanguageDetectionError: If there is an error during language detection
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
                    "Message must contain 'code' field for language detection"
                )
            
            code = message['code']
            if not isinstance(code, str):
                raise AgentMessageError(
                    self._name,
                    message_type,
                    "Code must be a string"
                )
            
            # Detect language
            language_scores = self._detect_language(code)
            
            # Find the most likely language
            detected_language = max(language_scores.items(), key=lambda x: x[1])
            language_name = detected_language[0]
            confidence = detected_language[1]
            
            # Check if we can detect this language
            if language_name != "unknown" and self._detectable_languages and language_name not in self._detectable_languages:
                raise LanguageDetectionError(
                    self._name,
                    f"Cannot detect language: {language_name} is not in the list of detectable languages",
                    language=language_name
                )
            
            # In a real implementation, this would provide more detailed analysis
            # For now, we return a placeholder response
            code_snippet = code[:30] + "..." if len(code) > 30 else code
            
            return {
                'type': 'language_detection',
                'content': f"Language Detection Agent {self._name} has analyzed your code: '{code_snippet}'",
                'sender': self._name,
                'recipient': message.get('sender', 'user'),
                'timestamp': self._get_timestamp(),
                'detected_language': language_name,
                'confidence': confidence,
                'language_scores': language_scores
            }
        except (AgentMessageError, LanguageDetectionError) as e:
            # Re-raise specialized exceptions
            logger.error(f"Error in language detection: {str(e)}")
            raise
        except Exception as e:
            # Wrap other exceptions
            logger.error(f"Unexpected error generating language detection response: {str(e)}")
            raise LanguageDetectionError(
                self._name,
                f"Failed to detect language: {str(e)}",
                language="unknown"
            )
