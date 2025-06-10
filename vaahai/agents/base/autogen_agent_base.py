"""
AutoGen-specific base agent class for VaahAI.

This module defines the base class for agents that use Microsoft's AutoGen framework.
"""

import os
from typing import Any, Dict, Optional, List

# Use optional import for AutoGen to allow tests to run without it
try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    autogen = None

from vaahai.agents.base.agent_base import AgentBase
from vaahai.config.manager import ConfigManager


class AutoGenAgentBase(AgentBase):
    """
    Base class for AutoGen-based agents.
    
    This class extends the AgentBase class with AutoGen-specific functionality,
    including LLM configuration and agent creation.
    
    Attributes:
        config (Dict[str, Any]): Configuration dictionary for the agent.
        name (str): Name of the agent.
        llm_config (Dict[str, Any]): LLM configuration for the AutoGen agent.
        agent: The underlying AutoGen agent instance.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the AutoGen agent with the given configuration.
        
        Args:
            config: Configuration dictionary for the agent.
        """
        if not AUTOGEN_AVAILABLE and not config.get("_test_mode", False):
            raise ImportError(
                "The autogen package is required for AutoGenAgentBase. "
                "Install it with: pip install pyautogen"
            )
            
        super().__init__(config)
        self.llm_config = self._prepare_llm_config()
        self.agent = self._create_autogen_agent()
    
    def _prepare_llm_config(self) -> Dict[str, Any]:
        """
        Prepare the LLM configuration for the agent.
        
        This method retrieves the LLM configuration from the VaahAI configuration
        system and merges it with any agent-specific configuration.
        
        Returns:
            Dict[str, Any]: LLM configuration dictionary.
        """
        try:
            # If in test mode, return a mock config
            if self.config.get("_test_mode", False):
                return {
                    "model": "test-model",
                    "temperature": 0.7,
                    "api_key": "test-api-key"
                }
                
            config_manager = ConfigManager()
            
            # Get provider from config or use default
            provider = self.config.get("provider", "openai")
            
            # Get model from config or use default
            model = self.config.get("model")
            if not model:
                # Try to get default model for provider
                provider_config = config_manager.get(f"providers.{provider}", {})
                model = provider_config.get("default_model", "gpt-4")
            
            # Get API key from configuration
            provider_config = config_manager.get(f"providers.{provider}", {})
            api_key = provider_config.get("api_key")
            
            if not api_key:
                # Try environment variable as fallback
                env_var_name = f"VAAHAI_PROVIDERS_{provider.upper()}_API_KEY"
                api_key = os.environ.get(env_var_name)
                
                if not api_key:
                    raise ValueError(f"No API key found for provider '{provider}'")
            
            # Default LLM config
            llm_config = {
                "model": model,
                "temperature": self.config.get("temperature", 0.7),
                "api_key": api_key
            }
            
            # Add any additional configuration from the agent config
            if "llm_config" in self.config:
                llm_config.update(self.config["llm_config"])
            
            return llm_config
            
        except Exception as e:
            raise ValueError(f"Error preparing LLM configuration: {str(e)}")
    
    def _create_autogen_agent(self) -> Any:
        """
        Create the underlying AutoGen agent.
        
        This method must be implemented by subclasses to create the specific
        type of AutoGen agent needed.
        
        Returns:
            Any: An AutoGen agent instance.
        """
        raise NotImplementedError("Subclasses must implement _create_autogen_agent()")
    
    def update_system_message(self, system_message: str) -> None:
        """
        Update the system message for the agent.
        
        Args:
            system_message: New system message for the agent.
        """
        if self.config.get("_test_mode", False):
            return
            
        if hasattr(self.agent, "update_system_message"):
            self.agent.update_system_message(system_message)
        else:
            raise NotImplementedError("The underlying agent does not support updating system messages")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history for the agent.
        
        Returns:
            List[Dict[str, Any]]: List of messages in the conversation history.
        """
        if self.config.get("_test_mode", False):
            return []
            
        if hasattr(self.agent, "chat_history"):
            return self.agent.chat_history
        elif hasattr(self.agent, "messages"):
            return self.agent.messages
        else:
            return []
