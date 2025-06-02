# Autogen Framework Integration

This document outlines the architecture and implementation details for integrating Microsoft's Autogen framework into Vaahai to create a sophisticated multi-agent system for code review.

## Overview

Vaahai is integrating Autogen to leverage a multi-agent approach to code review, where specialized agents collaborate to provide comprehensive analysis of code. This approach allows for more sophisticated and thorough reviews by distributing different aspects of code analysis to specialized agents.

## MVP Implementation: Hello World Agent

Before implementing the full multi-agent system, we've created a simple Hello World agent as a Minimum Viable Product (MVP) to validate the Autogen integration framework.

### Hello World Agent Structure

```
vaahai/
├── core/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py          # Base agent class
│   │   ├── hello_world.py   # Hello World agent implementation
│   │   └── factory.py       # Simple agent factory
├── cli/
│   ├── commands/
│   │   ├── __init__.py
│   │   └── helloworld.py    # CLI command implementation
```

### Base Agent Class

```python
# core/agents/base.py
class VaahaiAgent:
    """Base class for all Vaahai agents."""
    
    def __init__(self, config=None):
        """Initialize the agent with configuration."""
        self.config = config or {}
        
    def run(self, *args, **kwargs):
        """Run the agent with the given arguments."""
        raise NotImplementedError("Subclasses must implement run method")
```

### Hello World Agent Implementation

```python
# core/agents/hello_world.py
from .base import VaahaiAgent

class HelloWorldAgent(VaahaiAgent):
    """Simple Hello World agent for testing the Autogen integration."""
    
    def __init__(self, config=None):
        """Initialize the Hello World agent."""
        super().__init__(config)
        self.message = self.config.get("message", "Hello, World!")
        
    def run(self, *args, **kwargs):
        """Run the Hello World agent."""
        return {
            "success": True,
            "message": self.message,
            "agent_type": "hello_world"
        }
```

### Agent Factory

```python
# core/agents/factory.py
from .base import VaahaiAgent
from .hello_world import HelloWorldAgent

class AgentFactory:
    """Factory for creating Vaahai agents."""
    
    @staticmethod
    def create_agent(agent_type, config=None):
        """Create an agent of the specified type."""
        agents = {
            "hello_world": HelloWorldAgent
        }
        
        agent_class = agents.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_class(config)
```

### CLI Integration

```python
# cli/commands/helloworld.py
import typer
from vaahai.core.agents.factory import AgentFactory

app = typer.Typer()

@app.command()
def helloworld(
    message: str = typer.Option(None, "--message", "-m", help="Custom hello world message")
):
    """Run a simple Hello World agent to test the Autogen integration."""
    config = {}
    if message:
        config["message"] = message
    
    agent = AgentFactory.create_agent("hello_world", config)
    result = agent.run()
    
    typer.echo(result["message"])
    
    return result
```

### Usage

```bash
# Run with default message
vaahai helloworld

# Run with custom message
vaahai helloworld --message "Hello, Vaahai!"
```

## Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────────┐
│                    Review Coordinator Agent                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Group Chat Manager                       │
└───────┬───────────────┬────────────────┬────────────┬───────────┘
        │               │                │            │
        ▼               ▼                ▼            ▼
┌───────────┐   ┌───────────────┐  ┌──────────┐  ┌──────────────┐
│ Language  │   │ Framework/CMS │  │Standards │  │   Security   │
│ Detector  │   │   Detector    │  │ Analyzer │  │   Auditor    │
└───────────┘   └───────────────┘  └──────────┘  └──────────────┘
```

### Key Components

1. **Agent Factory**: Creates specialized agents based on configuration
2. **Review Orchestrator**: Manages the review process and agent collaboration
3. **Group Chat Manager**: Facilitates communication between agents
4. **Result Processor**: Processes and formats the results of the review

## Specialized Agents

### 1. Language Detector Agent

**Purpose**: Identify programming languages, features, and versions used in the code.

**Responsibilities**:
- Detect primary programming language(s)
- Identify language version indicators
- Recognize language-specific features and patterns

**Example Prompt**:
```
You are a Language Detector Agent specialized in identifying programming languages.
Analyze the following code and determine:
1. The primary programming language(s) used
2. Language version indicators if present
3. Any language-specific features or patterns

Code to analyze:
{code_snippet}
```

### 2. Framework/CMS Detector Agent

**Purpose**: Identify frameworks, libraries, and architectural patterns used in the code.

**Responsibilities**:
- Detect frameworks and libraries
- Identify architectural patterns (MVC, MVVM, etc.)
- Map dependencies and their relationships

**Example Prompt**:
```
You are a Framework Detector Agent specialized in identifying frameworks and libraries.
Analyze the following code and determine:
1. Frameworks or libraries being used
2. Architectural patterns (MVC, MVVM, etc.)
3. Key dependencies and their relationships

Code to analyze:
{code_snippet}
```

### 3. Standards Analyzer Agent

**Purpose**: Evaluate adherence to coding standards and best practices.

**Responsibilities**:
- Check adherence to language-specific coding standards
- Identify style inconsistencies
- Detect best practice violations

**Example Prompt**:
```
You are a Standards Analyzer Agent specialized in evaluating adherence to coding standards.
Analyze the following code and determine:
1. Adherence to language-specific coding standards
2. Style consistency issues
3. Best practice violations

Code to analyze:
{code_snippet}
```

### 4. Security Auditor Agent

**Purpose**: Identify security vulnerabilities and recommend improvements.

**Responsibilities**:
- Detect security vulnerabilities
- Identify common security anti-patterns
- Recommend security improvements

**Example Prompt**:
```
You are a Security Auditor Agent specialized in identifying security vulnerabilities.
Analyze the following code and determine:
1. Security vulnerabilities
2. Common security anti-patterns
3. Security best practice violations

Code to analyze:
{code_snippet}
```

### 5. Review Coordinator Agent

**Purpose**: Orchestrate the review process and aggregate findings.

**Responsibilities**:
- Divide code into logical segments
- Route specific questions to specialized agents
- Aggregate findings and generate a comprehensive report

**Example Prompt**:
```
You are a Review Coordinator Agent responsible for orchestrating the code review process.
Your tasks include:
1. Dividing code into logical segments
2. Routing specific questions to specialized agents
3. Aggregating findings and generating a comprehensive report

Code to review:
{code_snippet}
```

## Implementation Plan

### Phase 1: Setup

1. Add Autogen as a dependency
2. Create basic agent infrastructure
   - Define base agent classes and interfaces
   - Implement agent factory for creating specialized agents
   - Create Docker-based code executor integration
3. Implement agent configuration loading

### Phase 2: Agent Development

1. Implement specialized agents
   - Language Detector Agent (Priority 1)
   - Framework/CMS Detector Agent
   - Standards Analyzer Agent
   - Security Auditor Agent
   - Review Coordinator Agent
2. Create prompt templates for each agent
   - Base templates for common analysis tasks
   - Language-specific templates for specialized analysis
3. Define agent capabilities and limitations

### Phase 3: Orchestration

1. Implement the coordinator agent
2. Define workflow between agents
3. Create fallback mechanisms

### Phase 4: Integration

1. Connect Autogen system to the CLI
2. Implement output formatting for agent results
3. Add configuration options for agent customization

## Docker-Based Code Execution

The Autogen integration includes Docker-based code execution capabilities to enable agents to run and debug code during the review process. This feature allows for:

1. **Dynamic Code Analysis**: Run code to identify runtime issues not visible in static analysis
2. **Verification of Fixes**: Test suggested fixes to ensure they resolve the identified issues
3. **Language-Specific Testing**: Execute code in appropriate language-specific Docker containers
4. **Secure Execution Environment**: Isolate code execution in containers for security

### Implementation Details

The Docker-based code execution is implemented through the `VaahaiDockerCommandLineCodeExecutor` class, which extends Autogen's `DockerCommandLineCodeExecutor` with Vaahai-specific features:

```python
class VaahaiDockerCommandLineCodeExecutor:
    """Docker-based code execution environment for Autogen agents."""
    
    def __init__(self, config: Dict[str, Any]):
        # Initialize with configuration for resource limits, timeouts, etc.
        pass
        
    def execute_code(self, code: str, language: str) -> Dict[str, Any]:
        # Execute code in a Docker container for the specified language
        # Returns execution results, stdout, stderr, and execution time
        pass
```

Key features of the implementation include:

1. **Language Detection Integration**: Works with the Language Detector Agent to select appropriate Docker images
2. **Resource Limiting**: Configurable memory and CPU limits to prevent resource abuse
3. **Security Controls**: Network isolation by default with optional network access
4. **Timeout Management**: Configurable execution timeouts to prevent infinite loops
5. **Container Lifecycle Management**: Automatic cleanup of containers after execution

### Docker Executor Configuration

```toml
[code_executor]
enabled = true
timeout = 60  # seconds
memory_limit = "512m"
cpu_limit = 1.0
network_enabled = false

[code_executor.languages]
python = "python:3.9-slim"
javascript = "node:16-alpine"
java = "openjdk:11-jdk-slim"
go = "golang:1.17-alpine"
rust = "rust:1.56-slim"
```

### Usage in CLI

The code execution capabilities can be controlled via CLI flags:

```bash
# Enable code execution during review
vaahai review path/to/file.py --execute-code

# Disable code execution (default)
vaahai review path/to/file.py --no-execute-code

# Specify custom Docker image for execution
vaahai review path/to/file.py --execute-code --docker-image="python:3.10-slim"

# Set resource limits
vaahai review path/to/file.py --execute-code --memory-limit=1g --cpu-limit=2.0

# Enable network access (disabled by default)
vaahai review path/to/file.py --execute-code --network-enabled
```

### Integration with Agents

The Docker-based code executor is integrated with the specialized agents in the following ways:

1. **Language Detector Agent**: Determines the appropriate language for code execution
2. **Framework Detector Agent**: Identifies required dependencies for execution
3. **Standards Analyzer Agent**: Verifies that code meets standards by running tests
4. **Security Auditor Agent**: Tests for security vulnerabilities through execution
5. **Review Coordinator Agent**: Orchestrates code execution requests between agents

## Configuration

### Agent Configuration Schema

```toml
[agents]
# Global agent settings
max_rounds = 10
termination_message = "REVIEW_COMPLETE"

[agents.language_detector]
name = "LanguageDetector"
model = "gpt-4"
temperature = 0.2
system_message = """You are a Language Detector Agent..."""

[agents.framework_detector]
name = "FrameworkDetector"
model = "gpt-4"
temperature = 0.3
system_message = """You are a Framework Detector Agent..."""

# Additional agent configurations...

[group_chat]
max_rounds = 10
speaker_selection_method = "auto"
```

## CLI Integration

The Autogen integration will be accessible through the existing `review` command with an additional `--agent-config` option to specify a custom agent configuration file:

```bash
vaahai review path/to/file.py --agent-config path/to/agent_config.toml
```

## Output Formats

The multi-agent system will support the same output formats as the current implementation:

1. **Terminal**: Rich terminal output with color coding
2. **Markdown**: Structured markdown for documentation
3. **HTML**: Web-friendly format with styling

## Future Enhancements

1. **Custom Agent Creation**: Allow users to define their own specialized agents
2. **Agent Memory**: Implement persistent memory for agents across reviews
3. **Multi-File Context**: Enable agents to understand relationships between multiple files
4. **Interactive Reviews**: Allow users to ask follow-up questions to specific agents
5. **Visualization**: Add visualization of agent collaboration and decision-making process
