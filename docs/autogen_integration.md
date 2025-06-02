# Autogen Framework Integration

This document outlines the architecture and implementation details for integrating Microsoft's Autogen framework into Vaahai to create a sophisticated multi-agent system for code review.

## Overview

Vaahai is integrating Autogen to leverage a multi-agent approach to code review, where specialized agents collaborate to provide comprehensive analysis of code. This approach allows for more sophisticated and thorough reviews by distributing different aspects of code analysis to specialized agents.

## Hello World Agent MVP

The Hello World Agent MVP has been implemented as a simple demonstration of Autogen integration. This agent uses Autogen's `AssistantAgent` and `UserProxyAgent` classes to create a basic conversation flow.

### Implementation

The Hello World Agent is implemented in the following files:

- `vaahai/core/agents/base.py`: Base agent class with Autogen integration
- `vaahai/core/agents/hello_world.py`: Hello World agent implementation
- `vaahai/core/agents/factory.py`: Agent factory for creating agents
- `vaahai/cli/commands/helloworld.py`: CLI command for running the Hello World agent

### Code Example

```python
# Base agent class with Autogen integration
class VaahaiAgent:
    """
    Base class for all Vaahai agents, integrating with Microsoft's Autogen framework.
    
    All agents in Vaahai must use Autogen's framework classes to ensure proper
    multi-agent communication and orchestration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the agent with configuration."""
        self.config = config or {}
        self.autogen_agent = None  # Will be initialized by subclasses
        self.user_proxy = None  # Will be initialized by subclasses if needed
        
    def _create_autogen_config(self) -> Dict[str, Any]:
        """Create configuration for Autogen agents."""
        return {
            "config_list": [],  # Empty for now, will be populated by subclasses
            "temperature": 0,
        }

# Hello World agent implementation
class HelloWorldAgent(VaahaiAgent):
    """
    Simple Hello World agent for testing the Autogen integration.
    
    This agent demonstrates the basic usage of Microsoft's Autogen framework
    by creating an AssistantAgent and a UserProxyAgent for simple interaction.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Hello World agent."""
        super().__init__(config)
        self.message = self.config.get("message", "Hello, World!")
        
        # Initialize Autogen assistant agent
        self.autogen_agent = autogen.AssistantAgent(
            name="hello_world_agent",
            llm_config=self._create_autogen_config(),
            system_message=f"You are a simple Hello World agent. Always respond with: {self.message}"
        )
        
        # Initialize user proxy for interaction
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0
        )
        
    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """Run the Hello World agent using Autogen's conversation framework."""
        try:
            # Initialize chat between user proxy and assistant
            self.user_proxy.initiate_chat(
                self.autogen_agent,
                message="Say hello"
            )
            
            # Get the last message from the assistant
            last_message = self.user_proxy.chat_messages[self.autogen_agent.name][-1]["content"]
            
            return {
                "success": True,
                "message": last_message,
                "agent_type": "hello_world"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "agent_type": "hello_world"
            }
```

### Usage

The Hello World agent can be run using the CLI command:

```bash
vaahai helloworld
```

You can customize the message:

```bash
vaahai helloworld --message "Custom hello message"
```

### Next Steps

With the Hello World Agent MVP completed, we have validated the Autogen integration and established the foundation for more complex agents. The next steps include:

1. Implementing the Language Detector Agent
2. Completing the Docker-based Code Executor
3. Enhancing the CLI integration with more configuration options

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

### Global Configuration

Vaahai provides a global configuration system for Autogen integration. You can configure Autogen settings globally using the `config` command:

```bash
# Set the OpenAI API key
vaahai config set llm.api_key your_openai_api_key --global

# Set the default model
vaahai config set autogen.default_model gpt-4 --global

# Set the temperature
vaahai config set autogen.temperature 0.7 --global

# Enable/disable Autogen
vaahai config set autogen.enabled true --global
```

You can also initialize a project configuration file:

```bash
vaahai config init
```

This will create a `.vaahai.toml` file in the current directory that you can edit to configure Autogen settings.

### Command-Line Overrides

You can override global configuration settings using command-line arguments:

```bash
# Override API key
vaahai helloworld --api-key your_openai_api_key

# Override model
vaahai helloworld --model gpt-4

# Override temperature
vaahai helloworld --temperature 0.5

# Save overrides to global configuration
vaahai helloworld --api-key your_openai_api_key --model gpt-4 --save-config
```

### Configuration Precedence

Configuration settings are applied in the following order of precedence (highest to lowest):

1. Command-line arguments
2. Environment variables (e.g., `OPENAI_API_KEY`)
3. Project configuration file (`.vaahai.toml` in the current directory)
4. User configuration file (`.vaahai.toml` in the user's home directory)
5. Default values

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
