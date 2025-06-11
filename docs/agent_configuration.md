# Agent Configuration Guide

This guide explains how to configure agents in the VaahAI system, including the schema validation requirements for each agent type.

## Agent Configuration Overview

VaahAI uses a JSON schema validation system to ensure that agent configurations are valid before agent instantiation. This provides early detection of configuration errors and improves the robustness of the agent system.

## Base Agent Configuration

All agents in VaahAI require the following base configuration properties:

```json
{
  "name": "My Agent",  // A descriptive name for the agent
  "type": "conversational"  // The type of agent to create (required)
}
```

The `type` field is mandatory and must match one of the registered agent types in the system.

## Agent Types

VaahAI supports the following agent types:

### Conversational Agent

```json
{
  "name": "My Conversational Agent",
  "type": "conversational",
  "max_history_length": 10  // Optional: Maximum number of messages to keep in history
}
```

### Assistant Agent

```json
{
  "name": "My Assistant Agent",
  "type": "assistant",
  "system_prompt": "You are a helpful assistant.",  // Optional: System prompt for the assistant
  "tools": []  // Optional: List of tools available to the assistant
}
```

### User Proxy Agent

```json
{
  "name": "My User Proxy Agent",
  "type": "user_proxy",
  "human_input_mode": "ALWAYS"  // Optional: When to request human input
}
```

### Specialized Agents

Specialized agents extend the base agent configuration with domain-specific properties:

```json
{
  "name": "My Specialized Agent",
  "type": "specialized",
  "domain": "my_domain",  // Required: The domain of expertise
  "expertise": ["python", "web_development"]  // Required: List of expertise areas
}
```

#### Code Review Agent

```json
{
  "name": "My Code Review Agent",
  "type": "code_review",
  "domain": "code_quality",  // Required
  "expertise": ["python", "code_review"],  // Required: List of expertise areas
  "languages": ["python", "javascript"],  // Optional: Programming languages to review
  "review_criteria": ["style", "complexity"]  // Optional: Criteria to focus on
}
```

#### Security Audit Agent

```json
{
  "name": "My Security Audit Agent",
  "type": "security_audit",
  "domain": "security",  // Required
  "expertise": ["web_security", "penetration_testing"],  // Required: List of expertise areas
  "compliance_standards": ["OWASP", "PCI-DSS"],  // Optional: Compliance standards to check
  "vulnerability_categories": ["injection", "xss"]  // Optional: Vulnerability types to focus on
}
```

#### Language Detection Agent

```json
{
  "name": "My Language Detection Agent",
  "type": "language_detection",
  "domain": "language_analysis",  // Required
  "expertise": ["programming_languages", "syntax_analysis"],  // Required: List of expertise areas
  "detectable_languages": ["python", "javascript", "java"]  // Optional: Languages to detect
}
```

#### Report Generation Agent

```json
{
  "name": "My Report Generation Agent",
  "type": "report_generation",
  "domain": "reporting",  // Required
  "expertise": ["technical_documentation", "data_visualization"],  // Required: List of expertise areas
  "supported_formats": ["markdown", "html"],  // Optional: Output formats
  "visualization_types": ["table", "chart"]  // Optional: Visualization types
}
```

## Schema Validation

VaahAI validates agent configurations against JSON schemas defined in `vaahai/agents/schemas.py`. The validation occurs during agent initialization and will raise an `AgentInitializationError` if the configuration is invalid.

### Common Validation Errors

1. **Missing required fields**: Ensure all required fields are present in your configuration.
2. **Type mismatches**: Ensure field values match the expected types (e.g., `expertise` must be an array of strings).
3. **Unknown agent type**: Ensure the `type` field matches one of the registered agent types.

### Validation in Code

If you're creating agents programmatically, you can validate configurations before instantiation:

```python
from vaahai.agents.schema_validator import validate_agent_config

config = {
    "name": "My Agent",
    "type": "conversational"
}

# Validate the configuration
is_valid, errors = validate_agent_config(config)
if not is_valid:
    print(f"Configuration errors: {errors}")
else:
    # Create the agent
    from vaahai.agents.factory import AgentFactory
    agent = AgentFactory.create_agent("conversational", config)
```

## Configuration via TOML Files

When configuring agents via TOML configuration files, use the following format:

```toml
[agents.my_agent]
name = "My Agent"
type = "conversational"
max_history_length = 10

[agents.my_assistant]
name = "My Assistant"
type = "assistant"
system_prompt = "You are a helpful assistant."
tools = []

[agents.my_specialized_agent]
name = "My Specialized Agent"
type = "code_review"
domain = "code_quality"
expertise = ["python", "code_review"]
languages = ["python", "javascript"]
review_criteria = ["style", "complexity"]
```

## Best Practices

1. **Always specify the agent type**: The `type` field is required for all agent configurations.
2. **Use arrays for expertise**: The `expertise` field in specialized agents must be an array of strings.
3. **Provide descriptive names**: Use clear, descriptive names for your agents to make them easier to identify.
4. **Validate configurations early**: Validate configurations before creating agents to catch errors early.
