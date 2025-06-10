# VaahAI Prompt Management

This document describes the prompt management system used in VaahAI agents.

## Overview

The prompt management system provides a way to create, load, and render prompt templates for agents. It uses Jinja2 for template rendering and supports both agent-specific and shared prompt templates.

## Directory Structure

Prompt templates are stored in the following locations, in order of precedence:

1. Agent-specific prompts: `vaahai/agents/core/<agent_type>/prompts/` or `vaahai/agents/applications/<agent_type>/prompts/`
2. Shared prompts: `vaahai/agents/prompts/`

## Creating Prompt Templates

Prompt templates are markdown files with Jinja2 template syntax. For example:

```markdown
# {{ agent_name }} System Prompt

You are a {{ agent_role }} AI assistant.

## Your Task
{{ task_description }}

## Guidelines
{% for guideline in guidelines %}
- {{ guideline }}
{% endfor %}
```

## Using the Prompt Manager

```python
from vaahai.agents.utils.prompt_manager import PromptManager

# Create a prompt manager for a specific agent type
manager = PromptManager("hello_world")

# Render a prompt template with context variables
prompt = manager.render_prompt("greeting", {
    "user_greeting": "Hi there!",
    "agent_name": "Vaahai",
    "agent_role": "friendly"
})

# List available templates
templates = manager.list_templates()

# Get the path to a template file
template_path = manager.get_template_path("greeting")
```

## Template Inheritance

You can use Jinja2's template inheritance to create reusable prompt components:

```markdown
{% extends "base_system.md" %}

{% block guidelines %}
- Be concise and clear
- Use simple language
- Provide examples when possible
{% endblock %}
```

## Best Practices

1. **Keep prompts modular**: Split complex prompts into smaller, reusable components
2. **Use variables**: Make prompts flexible with context variables
3. **Include clear instructions**: Provide explicit guidelines in each prompt
4. **Version control**: Track changes to prompts in git
5. **Test thoroughly**: Verify that prompts produce the expected agent behavior

## API Reference

### PromptManager

```python
class PromptManager:
    def __init__(self, agent_type: str, agent_name: Optional[str] = None):
        """
        Initialize the prompt manager.
        
        Args:
            agent_type: Type of agent (e.g., "code_executor", "hello_world")
            agent_name: Optional custom name for the agent (defaults to agent_type)
        """
        
    def render_prompt(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render a prompt template with the given context.
        
        Args:
            template_name: Name of the template (without extension)
            context: Dictionary of variables to use in the template
            
        Returns:
            The rendered template as a string
            
        Raises:
            ValueError: If the template cannot be found or rendered
        """
        
    def get_template_path(self, template_name: str) -> Optional[str]:
        """
        Get the path to a template file.
        
        Args:
            template_name: Name of the template (without extension)
            
        Returns:
            The full path to the template file, or None if not found
        """
        
    def list_templates(self) -> List[str]:
        """
        List all available templates.
        
        Returns:
            List of template names (without extensions)
        """
```
