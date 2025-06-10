"""
AutoGen-specific base agent class for VaahAI.

This module defines the base class for agents that use Microsoft's AutoGen framework.
"""

import os
from typing import Any, Dict, Optional, List
import logging

# Try to import the required packages for the new autogen structure
try:
    from autogen_agentchat.agents import Agent
    from autogen_ext.models import ModelClient
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    AUTOGEN_PACKAGES_AVAILABLE = True
except ImportError:
    # Set flag to indicate packages are not available
    AUTOGEN_PACKAGES_AVAILABLE = False
    # Define dummy classes for type hints
    class Agent: pass
    class ModelClient: pass
    class OpenAIChatCompletionClient: pass
    
    # Only raise error if not in test mode
    logging.warning(
        "autogen-agentchat/autogen-ext packages not found. "
        "Running in test mode only. To use full functionality, install: "
        "pip install autogen-agentchat autogen-ext"
    )

# Import internal modules
from vaahai.cli.utils.config import load_config, get_config_value

# Set up logging
logger = logging.getLogger(__name__)


class AgentBase:
    """Abstract base class for all agents in the system."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent with a configuration.
        
        Args:
            config: Dictionary containing agent configuration
        """
        self.config = config
    
    def run(self, *args, **kwargs) -> Any:
        """
        Run the agent with the provided inputs.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            The result of running the agent
        """
        raise NotImplementedError("Subclasses must implement run()")


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
        # Check if we're in test mode
        test_mode = config.get("_test_mode", False)
        
        # If packages are not available and not in test mode, raise error
        if not AUTOGEN_PACKAGES_AVAILABLE and not test_mode:
            raise ImportError(
                "The autogen-agentchat and autogen-ext packages are required for AutoGenAgentBase. "
                "Install them with: pip install autogen-agentchat autogen-ext"
            )
            
        super().__init__(config)
        
        # Don't prepare LLM config in test mode
        if not test_mode:
            self.llm_config = self._prepare_llm_config()
        else:
            self.llm_config = {"model": "gpt-3.5-turbo"}
        
        # Initialize agent to None - subclasses will create it when ready
        self.agent = None
    
    def _prepare_llm_config(self) -> Dict[str, Any]:
        """
        Prepare the LLM configuration for the agent.
        
        This method retrieves the LLM configuration from the VaahAI configuration
        system and merges it with any agent-specific configuration.
        
        Returns:
            Dict[str, Any]: LLM configuration dictionary.
        """
        # Skip LLM config in test mode
        if self.config.get("_test_mode", False):
            return {"model": "gpt-3.5-turbo"}
            
        try:
            vaahai_config = load_config()
            provider = self.config.get("provider", "openai")
            model = self.config.get("model")
            
            if not model:
                model = get_config_value("llm.model", vaahai_config) or "gpt-4"
                
            # Get API key from config or environment variables
            api_key = get_config_value("llm.api_key", vaahai_config)
            if not api_key:
                # Check environment variables in order of precedence
                env_var_name = f"VAAHAI_PROVIDERS_{provider.upper()}_API_KEY"
                api_key = os.environ.get(env_var_name)
                
                # For OpenAI, also check standard environment variable
                if not api_key and provider.lower() == "openai":
                    api_key = os.environ.get("OPENAI_API_KEY")
                    
                if not api_key:
                    raise ValueError(f"No API key found for provider '{provider}'")
            
            # Prepare base LLM config
            llm_config = {
                "model": model,
                "temperature": self.config.get("temperature", 0.7),
                "api_key": api_key
            }
            
            # Handle API base URL
            api_base = os.environ.get(f"VAAHAI_PROVIDERS_{provider.upper()}_API_BASE")
            if not api_base and provider.lower() == "openai":
                api_base = os.environ.get("OPENAI_API_BASE")
                
            if api_base:
                llm_config["api_base"] = api_base
                
            # For project-specific keys (sk-proj-), set API type to azure
            if api_key and api_key.startswith("sk-proj-"):
                llm_config["api_type"] = "azure"
                
            # Update with any additional LLM config from agent config
            if "llm_config" in self.config:
                llm_config.update(self.config["llm_config"])
                
            return llm_config
            
        except Exception as e:
            raise ValueError(f"Error preparing LLM configuration: {str(e)}")

    def _create_model_client(self) -> Optional[ModelClient]:
        """
        Create a model client based on the LLM configuration.
        
        Returns:
            A model client for the agent to use
        """
        # Skip in test mode
        if self.config.get("_test_mode", False):
            return None
            
        # Skip if packages are not available
        if not AUTOGEN_PACKAGES_AVAILABLE:
            return None
            
        # Create OpenAI client
        if self.config.get("provider", "openai").lower() == "openai":
            client = OpenAIChatCompletionClient(
                model=self.llm_config.get("model", "gpt-3.5-turbo"),
                api_key=self.llm_config.get("api_key"),
            )
            
            # Set API base if provided
            if "api_base" in self.llm_config:
                client.api_base = self.llm_config["api_base"]
                
            return client
            
        return None
    
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
