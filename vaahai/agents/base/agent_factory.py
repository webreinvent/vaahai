"""
Agent factory for VaahAI.

This module provides a factory for creating and configuring agents.
"""

from typing import Any, Dict, List, Optional, Type
from vaahai.agents.base.agent_base import AgentBase
from vaahai.agents.base.agent_registry import AgentRegistry


class AgentFactory:
    """
    Factory for creating and configuring agents.
    
    This class provides methods for creating agents based on their type and
    configuration.
    """
    
    @staticmethod
    def create_agent(agent_type: str, config: Optional[Dict[str, Any]] = None) -> AgentBase:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: The type identifier for the agent.
            config: Configuration dictionary for the agent.
            
        Returns:
            AgentBase: An instance of the specified agent type.
            
        Raises:
            ValueError: If the agent type is not registered.
        """
        agent_class = AgentRegistry.get_agent_class(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_class(config or {})
    
    @staticmethod
    def create_agents(agent_configs: Dict[str, Dict[str, Any]]) -> Dict[str, AgentBase]:
        """
        Create multiple agents from a configuration dictionary.
        
        Args:
            agent_configs: A dictionary mapping agent names to their configurations.
            
        Returns:
            Dict[str, AgentBase]: A dictionary mapping agent names to agent instances.
            
        Raises:
            ValueError: If an agent type is missing or not registered.
        """
        agents = {}
        for agent_name, agent_config in agent_configs.items():
            agent_type = agent_config.get("type")
            if not agent_type:
                raise ValueError(f"Missing agent type for {agent_name}")
            
            agents[agent_name] = AgentFactory.create_agent(agent_type, agent_config)
        
        return agents
    
    @staticmethod
    def list_available_agents() -> List[str]:
        """
        List all available agent types.
        
        Returns:
            List[str]: A list of all registered agent type identifiers.
        """
        return AgentRegistry.list_agent_types()
    
    @staticmethod
    def is_agent_available(agent_type: str) -> bool:
        """
        Check if an agent type is available.
        
        Args:
            agent_type: The type identifier for the agent.
            
        Returns:
            bool: True if the agent type is registered, False otherwise.
        """
        return AgentRegistry.is_registered(agent_type)
