#!/usr/bin/env python
"""
Example script demonstrating the use of the PromptManager.

This script shows how to create a PromptManager instance, render prompt templates,
and use the rendered prompts with an LLM.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from vaahai.agents.utils.prompt_manager import PromptManager


def main():
    """Run the example."""
    print("VaahAI Prompt Manager Example\n")
    
    # Create a prompt manager for the "hello_world" agent
    prompt_manager = PromptManager("hello_world")
    
    # List available templates
    print("Available templates:")
    templates = prompt_manager.list_templates()
    for template in templates:
        print(f"- {template}")
    print()
    
    # Render the base_system template
    print("Rendering base_system template:")
    system_prompt = prompt_manager.render_prompt("base_system", {
        "agent_name": "VaahAI",
        "agent_role": "helpful assistant",
        "task_description": "Help users with their questions and tasks.",
        "guidelines": [
            "Be concise and clear",
            "Use simple language",
            "Provide examples when possible"
        ],
        "additional_info": "This is a demonstration of the prompt manager."
    })
    print(system_prompt)
    print()
    
    # Render the hello_world template
    print("Rendering hello_world template:")
    hello_prompt = prompt_manager.render_prompt("hello_world", {
        "user_greeting": "Hi there! How are you today?"
    })
    print(hello_prompt)
    print()
    
    # Get the path to a template
    template_path = prompt_manager.get_template_path("base_system")
    print(f"Path to base_system template: {template_path}")


if __name__ == "__main__":
    main()
