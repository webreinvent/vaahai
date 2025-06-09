"""
Configuration schema for VaahAI.

This module defines the schema for VaahAI configuration, which is used for validation
and documentation purposes. The schema defines the structure, types, and constraints
for configuration values.
"""

from typing import Dict, Any, List, Union, Optional
from dataclasses import dataclass, field


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI provider."""
    
    api_key: str = ""
    api_base: str = ""
    organization: str = ""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4000


@dataclass
class ClaudeConfig:
    """Configuration for Anthropic Claude provider."""
    
    api_key: str = ""
    model: str = "claude-3-sonnet-20240229"
    temperature: float = 0.7
    max_tokens: int = 4000


@dataclass
class JunieConfig:
    """Configuration for Junie provider."""
    
    api_key: str = ""
    model: str = "junie-8b"
    temperature: float = 0.7
    max_tokens: int = 4000


@dataclass
class OllamaConfig:
    """Configuration for Ollama provider."""
    
    api_base: str = "http://localhost:11434"
    model: str = "llama3"
    temperature: float = 0.7
    max_tokens: int = 4000


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""
    
    provider: str = "openai"
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    claude: ClaudeConfig = field(default_factory=ClaudeConfig)
    junie: JunieConfig = field(default_factory=JunieConfig)
    ollama: OllamaConfig = field(default_factory=OllamaConfig)


@dataclass
class DockerResourceLimits:
    """Resource limits for Docker containers."""
    
    cpu: float = 2.0
    memory: str = "2g"


@dataclass
class DockerConfig:
    """Configuration for Docker execution environment."""
    
    enabled: bool = True
    image: str = "vaahai/execution:latest"
    resource_limits: DockerResourceLimits = field(default_factory=DockerResourceLimits)


@dataclass
class OutputConfig:
    """Configuration for output formatting."""
    
    format: str = "terminal"
    verbosity: str = "normal"
    color: bool = True


@dataclass
class AgentConfig:
    """Configuration for AI agents."""
    
    timeout: int = 300
    max_iterations: int = 10
    memory: bool = True
    logging: bool = True


@dataclass
class VaahAIConfig:
    """Root configuration for VaahAI."""
    
    llm: LLMConfig = field(default_factory=LLMConfig)
    docker: DockerConfig = field(default_factory=DockerConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)


def validate_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate a configuration dictionary against the schema.
    
    Args:
        config (Dict[str, Any]): Configuration dictionary to validate
    
    Returns:
        List[str]: List of validation errors, empty if valid
    """
    errors = []
    
    # Validate LLM provider
    provider = config.get("llm", {}).get("provider", "")
    if provider not in ["openai", "claude", "junie", "ollama"]:
        errors.append(f"Invalid LLM provider: {provider}")
    
    # Validate output format
    output_format = config.get("output", {}).get("format", "")
    if output_format not in ["terminal", "markdown", "html", "json"]:
        errors.append(f"Invalid output format: {output_format}")
    
    # Validate verbosity
    verbosity = config.get("output", {}).get("verbosity", "")
    if verbosity not in ["quiet", "normal", "verbose", "debug"]:
        errors.append(f"Invalid verbosity level: {verbosity}")
    
    return errors


def config_to_schema(config: Dict[str, Any]) -> VaahAIConfig:
    """
    Convert a configuration dictionary to a schema object.
    
    Args:
        config (Dict[str, Any]): Configuration dictionary
    
    Returns:
        VaahAIConfig: Schema object
    """
    # Create the root config object
    schema_config = VaahAIConfig()
    
    # LLM configuration
    if "llm" in config:
        llm_config = config["llm"]
        if "provider" in llm_config:
            schema_config.llm.provider = llm_config["provider"]
        
        # OpenAI configuration
        if "openai" in llm_config:
            openai_config = llm_config["openai"]
            for key, value in openai_config.items():
                if hasattr(schema_config.llm.openai, key):
                    setattr(schema_config.llm.openai, key, value)
        
        # Claude configuration
        if "claude" in llm_config:
            claude_config = llm_config["claude"]
            for key, value in claude_config.items():
                if hasattr(schema_config.llm.claude, key):
                    setattr(schema_config.llm.claude, key, value)
        
        # Junie configuration
        if "junie" in llm_config:
            junie_config = llm_config["junie"]
            for key, value in junie_config.items():
                if hasattr(schema_config.llm.junie, key):
                    setattr(schema_config.llm.junie, key, value)
        
        # Ollama configuration
        if "ollama" in llm_config:
            ollama_config = llm_config["ollama"]
            for key, value in ollama_config.items():
                if hasattr(schema_config.llm.ollama, key):
                    setattr(schema_config.llm.ollama, key, value)
    
    # Docker configuration
    if "docker" in config:
        docker_config = config["docker"]
        if "enabled" in docker_config:
            schema_config.docker.enabled = docker_config["enabled"]
        if "image" in docker_config:
            schema_config.docker.image = docker_config["image"]
        if "resource_limits" in docker_config:
            resource_limits = docker_config["resource_limits"]
            if "cpu" in resource_limits:
                schema_config.docker.resource_limits.cpu = resource_limits["cpu"]
            if "memory" in resource_limits:
                schema_config.docker.resource_limits.memory = resource_limits["memory"]
    
    # Output configuration
    if "output" in config:
        output_config = config["output"]
        if "format" in output_config:
            schema_config.output.format = output_config["format"]
        if "verbosity" in output_config:
            schema_config.output.verbosity = output_config["verbosity"]
        if "color" in output_config:
            schema_config.output.color = output_config["color"]
    
    # Agent configuration
    if "agent" in config:
        agent_config = config["agent"]
        if "timeout" in agent_config:
            schema_config.agent.timeout = agent_config["timeout"]
        if "max_iterations" in agent_config:
            schema_config.agent.max_iterations = agent_config["max_iterations"]
        if "memory" in agent_config:
            schema_config.agent.memory = agent_config["memory"]
        if "logging" in agent_config:
            schema_config.agent.logging = agent_config["logging"]
    
    return schema_config


def schema_to_config(schema: VaahAIConfig) -> Dict[str, Any]:
    """
    Convert a schema object to a configuration dictionary.
    
    Args:
        schema (VaahAIConfig): Schema object
    
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    config = {
        "llm": {
            "provider": schema.llm.provider,
            "openai": {
                "api_key": schema.llm.openai.api_key,
                "api_base": schema.llm.openai.api_base,
                "organization": schema.llm.openai.organization,
                "model": schema.llm.openai.model,
                "temperature": schema.llm.openai.temperature,
                "max_tokens": schema.llm.openai.max_tokens
            },
            "claude": {
                "api_key": schema.llm.claude.api_key,
                "model": schema.llm.claude.model,
                "temperature": schema.llm.claude.temperature,
                "max_tokens": schema.llm.claude.max_tokens
            },
            "junie": {
                "api_key": schema.llm.junie.api_key,
                "model": schema.llm.junie.model,
                "temperature": schema.llm.junie.temperature,
                "max_tokens": schema.llm.junie.max_tokens
            },
            "ollama": {
                "api_base": schema.llm.ollama.api_base,
                "model": schema.llm.ollama.model,
                "temperature": schema.llm.ollama.temperature,
                "max_tokens": schema.llm.ollama.max_tokens
            }
        },
        "docker": {
            "enabled": schema.docker.enabled,
            "image": schema.docker.image,
            "resource_limits": {
                "cpu": schema.docker.resource_limits.cpu,
                "memory": schema.docker.resource_limits.memory
            }
        },
        "output": {
            "format": schema.output.format,
            "verbosity": schema.output.verbosity,
            "color": schema.output.color
        },
        "agent": {
            "timeout": schema.agent.timeout,
            "max_iterations": schema.agent.max_iterations,
            "memory": schema.agent.memory,
            "logging": schema.agent.logging
        }
    }
    
    return config
