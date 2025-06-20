"""
Language, framework, and CMS detection agent implementation.

This module provides an agent that uses the default LLM provider to detect
the programming language, framework, and CMS from code content.
"""

import json
import logging
from typing import Any, Dict, Optional

from vaahai.agents.base.agent_base import AgentBase
from vaahai.agents.base.agent_registry import AgentRegistry
from vaahai.config.manager import ConfigManager
from vaahai.utils.llm_client import get_llm_client

# Setup logging
logger = logging.getLogger(__name__)


@AgentRegistry.register("llm_detection")
class LLMLanguageFrameworkCMSDetectionAgent(AgentBase):
    """
    Uses the default LLM provider to detect language, framework, and CMS from code.
    
    This agent leverages LLM capabilities to analyze code content and determine
    the programming language, framework, and CMS being used. It returns a structured
    response with the detection results.
    
    Attributes:
        config (Dict[str, Any]): Configuration dictionary for the agent
        name (str): Name of the agent, defaults to class name if not specified
        llm_client: The LLM client to use for detection
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM Detection Agent.
        
        Args:
            config: Configuration dictionary for the agent
        """
        # Call parent's init first to set up self.config
        super().__init__(config)
        
        # Initialize config manager and LLM client
        self.config_manager = ConfigManager()
        default_provider = self.config_manager.get_default_llm_provider()
        self.llm_client = get_llm_client(default_provider)
        logger.debug(f"Initialized LLMLanguageFrameworkCMSDetectionAgent with provider: {default_provider}")
    
    def run(self, code: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect language, framework, and CMS from code content.
        
        Args:
            code (str): The code content to analyze
            file_path (Optional[str]): The file path (if available) for additional context
            
        Returns:
            Dict[str, Any]: A dictionary containing detection results with the following structure:
                {
                    "primary_language": {
                        "name": str,
                        "confidence": float
                    },
                    "primary_framework": {
                        "name": str,
                        "confidence": float
                    },
                    "primary_cms": {
                        "name": str,
                        "confidence": float
                    }
                }
        """
        logger.debug("Running LLM detection on code")
        
        # Build the prompt with file path context if available
        file_context = f"\nFile path: {file_path}" if file_path else ""
        prompt = (
            "Analyze the following code and strictly answer in this JSON format:\n"
            "{\n  \"language\": {\"name\": \"<main programming language>\", \"confidence\": <0.0-1.0>},\n"
            "  \"framework\": {\"name\": \"<main framework or null>\", \"confidence\": <0.0-1.0>},\n"
            "  \"cms\": {\"name\": \"<main CMS or null>\", \"confidence\": <0.0-1.0>}\n}\n"
            f"If framework or CMS are not detected, use null for the name and 0.0 for confidence.{file_context}\n"
            "Code:\n" + code
        )
        
        # Get response from LLM
        response = self.llm_client.complete(prompt)
        logger.debug(f"Received LLM response of length {len(response)}")
        
        # Try to extract JSON from the response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            result = json.loads(json_str.replace("'", '"'))
            
            # Format the response to match the expected structure
            detection_result = {
                "primary_language": result.get("language", {"name": "Unknown", "confidence": 0.0}),
                "primary_framework": result.get("framework", {"name": None, "confidence": 0.0}),
                "primary_cms": result.get("cms", {"name": None, "confidence": 0.0})
            }
            
            # Replace None/null with "Unknown" for consistency in the name field
            if detection_result["primary_language"]["name"] is None:
                detection_result["primary_language"]["name"] = "Unknown"
                
            logger.debug(f"Detection result: {detection_result}")
            return detection_result
            
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {e}")
            # Return a default response on error
            return {
                "primary_language": {"name": "Unknown", "confidence": 0.0},
                "primary_framework": {"name": None, "confidence": 0.0},
                "primary_cms": {"name": None, "confidence": 0.0}
            }
            
    def _validate_config(self) -> None:
        """Validate the agent configuration."""
        # No specific config validation needed for this agent
        pass
