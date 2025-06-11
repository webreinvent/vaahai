# Phase 2 Implementation Plan: First Tasks

This document outlines the detailed implementation plan for the first few tasks of Phase 2, focusing on getting the Hello World agent working as quickly as possible.

## Task Breakdown

### [P2-T1] Implement Base Agent Classes

#### Objective
Create the foundation for all agents in the VaahAI system by implementing abstract base classes and interfaces.

#### Steps
1. Create the directory structure:
   ```
   vaahai/
   └── agents/
       ├── base/
       │   ├── __init__.py
       │   ├── agent_base.py
       │   └── autogen_agent_base.py
       ├── __init__.py
   ```

2. Implement `agent_base.py` with the `AgentBase` abstract class:
   ```python
   from abc import ABC, abstractmethod
   from typing import Any, Dict, Optional

   class AgentBase(ABC):
       """Abstract base class for all VaahAI agents."""
       
       def __init__(self, config: Dict[str, Any]):
           self.config = config
           self.name = self.config.get("name", self.__class__.__name__)
           self.initialize()
       
       def initialize(self) -> None:
           """Initialize agent resources."""
           pass
       
       @abstractmethod
       def run(self, *args, **kwargs) -> Any:
           """Run the agent with the given inputs."""
           pass
       
       def cleanup(self) -> None:
           """Clean up any resources used by the agent."""
           pass
   ```

3. Implement `autogen_agent_base.py` with the `AutoGenAgentBase` class:
   ```python
   from typing import Any, Dict, Optional
   import autogen
   from vaahai.agents.base.agent_base import AgentBase
   from vaahai.config.manager import ConfigManager

   class AutoGenAgentBase(AgentBase):
       """Base class for AutoGen-based agents."""
       
       def __init__(self, config: Dict[str, Any]):
           super().__init__(config)
           self.llm_config = self._prepare_llm_config()
           self.agent = self._create_autogen_agent()
           
       def _prepare_llm_config(self) -> Dict[str, Any]:
           """Prepare the LLM configuration for the agent."""
           config_manager = ConfigManager()
           provider = self.config.get("provider", "openai")
           model = self.config.get("model", "gpt-4")
           
           # Get API key from configuration
           provider_config = config_manager.get("providers", {}).get(provider, {})
           api_key = provider_config.get("api_key")
           
           # Default LLM config
           return {
               "model": model,
               "temperature": self.config.get("temperature", 0.7),
               "api_key": api_key
           }
       
       def _create_autogen_agent(self) -> Any:
           """Create the underlying AutoGen agent."""
           raise NotImplementedError("Subclasses must implement _create_autogen_agent()")
   ```

4. Create unit tests for base agent classes:
   ```
   vaahai/test/unit/agents/
   ├── __init__.py
   ├── test_agent_base.py
   └── test_autogen_agent_base.py
   ```

#### Deliverables
- Base agent classes with proper abstraction
- Unit tests for base agent classes
- Documentation for extending base classes

### [P2-T2] Implement Agent Factory

#### Objective
Create a factory pattern for agent creation and registration to allow dynamic instantiation of agents.

#### Steps
1. Create the agent registry module:
   ```
   vaahai/agents/base/agent_registry.py
   ```

2. Implement the agent registry:
   ```python
   from typing import Dict, Type, Optional
   from vaahai.agents.base.agent_base import AgentBase

   class AgentRegistry:
       """Registry for agent types."""
       
       _registry: Dict[str, Type[AgentBase]] = {}
       
       @classmethod
       def register(cls, agent_type: str) -> callable:
           """Register an agent class with the registry."""
           def decorator(agent_class: Type[AgentBase]) -> Type[AgentBase]:
               cls._registry[agent_type] = agent_class
               return agent_class
           return decorator
       
       @classmethod
       def get_agent_class(cls, agent_type: str) -> Optional[Type[AgentBase]]:
           """Get an agent class by type."""
           return cls._registry.get(agent_type)
       
       @classmethod
       def list_agent_types(cls) -> list:
           """List all registered agent types."""
           return list(cls._registry.keys())
   ```

3. Create the agent factory module:
   ```
   vaahai/agents/base/agent_factory.py
   ```

4. Implement the agent factory:
   ```python
   from typing import Any, Dict, List, Optional, Type
   from vaahai.agents.base.agent_base import AgentBase
   from vaahai.agents.base.agent_registry import AgentRegistry

   class AgentFactory:
       """Factory for creating and configuring agents."""
       
       @staticmethod
       def create_agent(agent_type: str, config: Optional[Dict[str, Any]] = None) -> AgentBase:
           """Create an agent of the specified type."""
           agent_class = AgentRegistry.get_agent_class(agent_type)
           if not agent_class:
               raise ValueError(f"Unknown agent type: {agent_type}")
           
           return agent_class(config or {})
       
       @staticmethod
       def create_agents(agent_configs: Dict[str, Dict[str, Any]]) -> Dict[str, AgentBase]:
           """Create multiple agents from a configuration dictionary."""
           agents = {}
           for agent_name, agent_config in agent_configs.items():
               agent_type = agent_config.get("type")
               if not agent_type:
                   raise ValueError(f"Missing agent type for {agent_name}")
               
               agents[agent_name] = AgentFactory.create_agent(agent_type, agent_config)
           
           return agents
       
       @staticmethod
       def list_available_agents() -> List[str]:
           """List all available agent types."""
           return AgentRegistry.list_agent_types()
   ```

5. Create unit tests for the agent factory:
   ```
   vaahai/test/unit/agents/test_agent_factory.py
   ```

#### Deliverables
- Agent registry with decorator-based registration
- Agent factory with creation methods
- Unit tests for agent factory
- Documentation for registering and creating agents

### [P2-T4] Set Up Prompt Management

#### Objective
Create a system for loading and rendering prompt templates to ensure consistent agent behavior.

#### Steps
1. Create the prompt manager module:
   ```
   vaahai/agents/utils/prompt_manager.py
   ```

2. Implement the prompt manager:
   ```python
   import os
   from typing import Any, Dict, List, Optional
   from jinja2 import Environment, FileSystemLoader, select_autoescape

   class PromptManager:
       """Manages prompt templates for agents."""
       
       def __init__(self, agent_type: str, agent_name: Optional[str] = None):
           self.agent_type = agent_type
           self.agent_name = agent_name or agent_type
           self.prompt_dirs = self._get_prompt_directories()
           self.env = self._create_template_environment()
           
       def _get_prompt_directories(self) -> List[str]:
           """Get the directories containing prompt templates."""
           # Check if it's a core agent or application agent
           base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
           
           # Try to find the agent directory
           for agent_category in ["core", "applications"]:
               agent_dir = os.path.join(base_dir, agent_category, self.agent_type)
               if os.path.exists(agent_dir):
                   prompt_dir = os.path.join(agent_dir, "prompts")
                   if os.path.exists(prompt_dir):
                       return [prompt_dir]
           
           # If not found, return a default location
           return [os.path.join(base_dir, "prompts")]
       
       def _create_template_environment(self) -> Environment:
           """Create a Jinja2 template environment."""
           return Environment(
               loader=FileSystemLoader(self.prompt_dirs),
               autoescape=select_autoescape(['html', 'xml']),
               trim_blocks=True,
               lstrip_blocks=True
           )
       
       def render_prompt(self, template_name: str, context: Dict[str, Any]) -> str:
           """Render a prompt template with the given context."""
           try:
               template = self.env.get_template(f"{template_name}.md")
               return template.render(**context)
           except Exception as e:
               raise ValueError(f"Error rendering template {template_name}: {str(e)}")
       
       def get_template_path(self, template_name: str) -> Optional[str]:
           """Get the path to a template file."""
           for prompt_dir in self.prompt_dirs:
               path = os.path.join(prompt_dir, f"{template_name}.md")
               if os.path.exists(path):
                   return path
           return None
   ```

3. Create a directory for utility functions:
   ```
   vaahai/agents/utils/__init__.py
   ```

4. Create unit tests for the prompt manager:
   ```
   vaahai/test/unit/agents/utils/test_prompt_manager.py
   ```

#### Deliverables
- Prompt manager for loading and rendering templates
- Support for Jinja2 template syntax
- Unit tests for prompt manager
- Documentation for creating and using prompt templates

### [P2-T7] Implement Hello World Agent

#### Objective
Create a simple demonstration agent that responds to greetings in a humorous way.

#### Steps
1. Create the hello world agent directory structure:
   ```
   vaahai/agents/applications/hello_world/
   ├── __init__.py
   ├── agent.py
   └── prompts/
       └── greeting.md
   ```

2. Create the greeting prompt template:
   ```markdown
   # Hello World Agent Prompt

   You are a friendly and humorous AI assistant. Your job is to respond to greetings in a creative and funny way.

   ## Guidelines
   - Be friendly and welcoming
   - Include a joke or humorous comment in your response
   - Keep your response brief (2-3 sentences)
   - If the user mentions a specific topic, try to make your joke related to that topic
   - Always maintain a positive and uplifting tone

   ## User Input
   {{ user_input }}

   ## Response Format
   Start with a greeting, then include your humorous comment, and end with a question or invitation to continue the conversation.
   ```

3. Implement the hello world agent:
   ```python
   from typing import Any, Dict
   import autogen
   from vaahai.agents.base.agent_base import AutoGenAgentBase
   from vaahai.agents.base.agent_registry import AgentRegistry
   from vaahai.agents.utils.prompt_manager import PromptManager

   @AgentRegistry.register("hello_world")
   class HelloWorldAgent(AutoGenAgentBase):
       """A simple demonstration agent that responds to greetings in a humorous way."""
       
       def __init__(self, config: Dict[str, Any]):
           super().__init__(config)
           self.prompt_manager = PromptManager("hello_world")
       
       def _create_autogen_agent(self) -> Any:
           """Create an AutoGen AssistantAgent."""
           system_message = self.prompt_manager.render_prompt("greeting", {})
           
           return autogen.AssistantAgent(
               name=self.config.get("name", "HelloWorld"),
               system_message=system_message,
               llm_config=self.llm_config
           )
       
       def run(self, user_input: str) -> str:
           """Generate a humorous greeting response."""
           # Render the prompt with the user input
           context = {"user_input": user_input}
           system_message = self.prompt_manager.render_prompt("greeting", context)
           
           # Update the agent's system message
           self.agent.update_system_message(system_message)
           
           # Generate a response
           response = self.agent.generate_reply(
               messages=[{"role": "user", "content": user_input}],
               sender={"name": "User"}
           )
           
           return response
   ```

4. Create unit tests for the hello world agent:
   ```
   vaahai/test/unit/agents/applications/hello_world/test_hello_world_agent.py
   ```

5. Create a simple CLI command to test the hello world agent:
   ```
   vaahai/cli/commands/hello.py
   ```

6. Implement the hello command:
   ```python
   import typer
   from rich.panel import Panel
   from vaahai.agents.base.agent_factory import AgentFactory
   from vaahai.cli.utils.console import console

   app = typer.Typer(help="Hello world commands")

   @app.command("world")
   def hello_world(
       message: str = typer.Argument("Hello, world!", help="Message to send to the hello world agent")
   ):
       """
       Test the hello world agent with a greeting message.
       """
       try:
           # Create the hello world agent
           agent = AgentFactory.create_agent("hello_world", {
               "name": "HelloWorld",
               "temperature": 0.8  # Higher temperature for more creative responses
           })
           
           # Run the agent
           response = agent.run(message)
           
           # Display the response
           console.print(Panel(response, title="Hello World Agent", border_style="green"))
           
       except Exception as e:
           console.print(f"[bold red]Error:[/bold red] {str(e)}")
   ```

7. Register the hello command in the main CLI:
   ```python
   # In vaahai/cli/main.py
   from vaahai.cli.commands import hello
   
   app.add_typer(hello.app, name="hello", help="Hello world commands")
   ```

#### Deliverables
- Hello world agent implementation
- Greeting prompt template
- CLI command for testing the agent
- Unit tests for the hello world agent
- Documentation for using the hello world agent

## Implementation Order

To get the hello world agent working as quickly as possible, follow this implementation order:

1. **Base Agent Classes** [P2-T1]
   - Create directory structure
   - Implement `AgentBase` abstract class
   - Implement `AutoGenAgentBase` class
   - Write basic tests

2. **Agent Factory** [P2-T2]
   - Implement agent registry
   - Implement agent factory
   - Write basic tests

3. **Prompt Management** [P2-T4]
   - Implement prompt manager
   - Create utility functions
   - Write basic tests

4. **Hello World Agent** [P2-T7]
   - Create directory structure
   - Create greeting prompt template
   - Implement hello world agent
   - Create CLI command
   - Test the agent

## Testing Strategy

For each component, create unit tests that verify:

1. **Base Agent Classes**
   - Initialization with different configurations
   - Lifecycle methods (initialize, run, cleanup)
   - Error handling

2. **Agent Factory**
   - Agent registration
   - Agent creation with valid and invalid types
   - Multiple agent creation

3. **Prompt Management**
   - Template loading
   - Template rendering with different contexts
   - Error handling for missing templates

4. **Hello World Agent**
   - Agent creation
   - Response generation
   - CLI command execution

## Dependencies

Make sure the following dependencies are installed:

```
pip install pyautogen jinja2
```

Or add them to your `pyproject.toml`:

```toml
[tool.poetry.dependencies]
pyautogen = "^0.2.0"
jinja2 = "^3.1.2"
```

## Next Steps After Hello World

Once the hello world agent is working, proceed with:

1. **Group Chat Manager** [P2-T3]
2. **Tool Registry** [P2-T5]
3. **Agent Testing Framework** [P2-T6]
4. **Core Agents** (Code Executor, Formatter, Analyzer) [P2-T8, P2-T9, P2-T10]
