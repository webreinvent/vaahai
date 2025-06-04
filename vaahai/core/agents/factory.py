"""
Agent Factory

Factory pattern implementation for creating Vaahai agents.
"""

from typing import Dict, Any, Optional
from .base import VaahaiAgent, AUTOGEN_AVAILABLE
from .hello_world import HelloWorldAgent
from .language_detector import LanguageDetectorAgent


class AgentFactory:
    """Factory for creating Vaahai agents."""
    
    @staticmethod
    def create_agent(agent_type: str, config: Optional[Dict[str, Any]] = None) -> VaahaiAgent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create
            config: Configuration for the agent
            
        Returns:
            An instance of the specified agent type
            
        Raises:
            ValueError: If the agent type is unknown or if Autogen is not available
        """
        # Check if Autogen is available
        if not AUTOGEN_AVAILABLE:
            # We'll still allow creating the agent objects, but they'll have limited functionality
            # This allows commands like 'config init' to work even without Autogen dependencies
            pass
            
        agents = {
            "hello_world": HelloWorldAgent,
            "language_detector": LanguageDetectorAgent,
            # Add more agent types here as they are implemented
            # "framework_detector": FrameworkDetectorAgent,
            # "standards_analyzer": StandardsAnalyzerAgent,
            # "security_auditor": SecurityAuditorAgent,
            # "review_coordinator": ReviewCoordinatorAgent,
        }
        
        agent_class = agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_class(config)
