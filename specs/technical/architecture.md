# Vaahai Technical Architecture

## Overview

This document provides a detailed description of Vaahai's technical architecture, including component interactions, data flows, and implementation details. It serves as a guide for developers implementing the system.

## Architectural Style

Vaahai follows a modular, component-based architecture with the following characteristics:

1. **Layered Architecture**: Separation of concerns between CLI, business logic, and external integrations
2. **Plugin System**: Extensible architecture for analyzers, LLM providers, and formatters
3. **Command Pattern**: CLI commands encapsulate specific operations
4. **Dependency Injection**: Components receive dependencies rather than creating them
5. **Factory Pattern**: Dynamic creation of appropriate implementations based on configuration
6. **Multi-Agent Architecture**: Collaborative AI agents using Microsoft's Autogen framework

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       CLI Application (Typer)                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Configuration Manager                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    Code     │  │   Static    │  │   Review    │  │   Output    │
│   Scanner   │◄─┤  Analysis   │◄─┤ Orchestrator│◄─┤  Formatter  │
│             │  │ Integration │  │             │  │             │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │                │
       │                │                ▼                │
       │                │         ┌─────────────────┐    │
       │                │         │  Autogen-based  │    │
       │                │         │  Multi-Agent    │    │
       │                │         │  System         │    │
       │                │         └────────┬────────┘    │
       │                │                  │             │
       │                │                  ▼             │
       │                │         ┌─────────────┐        │
       │                │         │     LLM     │        │
       │                │         │  Providers  │        │
       │                │         └─────────────┘        │
       │                │                                │
       └────────────────┴────────────┬─────────────────┐│
                                     │                 ││
                                     ▼                 ▼▼
                              ┌─────────────┐  ┌─────────────┐
                              │ Interactive │  │   Report    │
                              │     Fix     │  │ Generation  │
                              └─────────────┘  └─────────────┘
```

## System Components

### Core Components

#### CLI Application

The CLI application serves as the entry point and user interface for Vaahai.

**Implementation Details**:
- Built using Typer framework for command-line parsing and interaction
- Implements commands for review, analysis, configuration, and help
- Handles argument parsing, validation, and command routing
- Manages user interaction for interactive features
- Coordinates the overall review process

**Key Classes**:
- `app`: Typer application instance
- `ReviewCommand`: Handles code review operations
- `AnalyzeCommand`: Handles static analysis operations
- `ConfigCommand`: Manages configuration operations

**Example Usage**:
```python
# CLI entry point
import typer
from vaahai.cli.commands import review, analyze, config

app = typer.Typer(
    name="vaahai",
    help="AI-augmented code review tool",
    add_completion=False,
)

app.add_typer(review.app, name="review", help="Review code with AI assistance")
app.add_typer(analyze.app, name="analyze", help="Run static analysis on code")
app.add_typer(config.app, name="config", help="Manage configuration")

if __name__ == "__main__":
    app()
```

#### Configuration Manager

The Configuration Manager handles loading, validating, and providing access to application settings.

**Implementation Details**:
- Loads configuration from multiple sources with precedence:
  1. Command-line arguments
  2. Project-level configuration file
  3. User-level configuration file
  4. Environment variables
  5. Default values
- Validates configuration against schema
- Securely handles sensitive information (API keys)
- Provides typed access to configuration values

**Key Classes**:
- `ConfigManager`: Central configuration management
- `ConfigSchema`: Pydantic model defining configuration structure
- `ConfigSource`: Abstract base class for configuration sources
- `FileConfigSource`, `EnvConfigSource`: Specific configuration sources

**Example Usage**:
```python
from vaahai.core.config import ConfigManager

# Initialize configuration
config_manager = ConfigManager()
config_manager.load()

# Access configuration values
api_key = config_manager.get("llm.openai.api_key")
review_depth = config_manager.get("review.depth", "standard")
```

#### Code Scanner

The Code Scanner identifies and processes code files for review.

**Implementation Details**:
- Resolves file paths, directory paths, and glob patterns
- Filters files based on inclusion/exclusion rules
- Handles large directories efficiently
- Extracts file metadata (size, language, encoding)
- Reads file contents with appropriate encoding

**Key Classes**:
- `CodeScanner`: Main scanning functionality
- `FileInfo`: Data class containing file metadata and content
- `LanguageDetector`: Identifies programming language from file

**Example Usage**:
```python
from vaahai.core.scanner import CodeScanner

scanner = CodeScanner()
files = scanner.scan("path/to/project", 
                    include=["*.py"], 
                    exclude=["*_test.py", "venv/*"])

for file_info in files:
    print(f"Found {file_info.language} file: {file_info.path}")
```

#### Review Orchestrator

The Review Orchestrator manages the Autogen multi-agent system to generate comprehensive code reviews.

**Implementation Details**:
- Initializes and configures Autogen agents and group chat
- Manages the multi-agent collaboration process
- Prepares code context and configuration for agents
- Processes and structures outputs from agent collaboration
- Handles token limitations through chunking
- Coordinates specialized agents for different aspects of code review

**Key Classes**:
- `ReviewOrchestrator`: Coordinates the multi-agent review process
- `AgentFactory`: Creates specialized agents based on configuration
- `ReviewGroupChatManager`: Manages agent communication
- `PromptBuilder`: Constructs prompts for agents
- `ReviewResult`: Structured representation of review output

**Example Usage**:
```python
from vaahai.core.orchestrator import ReviewOrchestrator
from vaahai.llm.providers import LLMProviderFactory

provider = LLMProviderFactory.create("openai")
orchestrator = ReviewOrchestrator(provider)

review_result = orchestrator.review_code(
    code="def example(): pass",
    language="python",
    static_analysis_results=analysis_results,
    review_depth="standard",
    agent_config=agent_config
)

print(review_result.summary)
for issue in review_result.issues:
    print(f"{issue.severity}: {issue.message} at line {issue.line}")
```

#### Autogen Multi-Agent System

The Autogen Multi-Agent System implements specialized agents that collaborate to perform comprehensive code review.

**Implementation Details**:
- Uses Microsoft's Autogen framework for agent creation and communication
- Implements specialized agents for different aspects of code review
- Enables collaborative analysis through agent communication
- Provides a flexible architecture for adding new agent types
- Supports customization of agent behavior through configuration

**Key Agents**:
- `LanguageDetectorAgent`: Identifies programming languages, features, and versions
- `FrameworkDetectorAgent`: Identifies frameworks, libraries, and architectural patterns
- `StandardsAnalyzerAgent`: Evaluates adherence to coding standards and best practices
- `SecurityAuditorAgent`: Identifies security vulnerabilities and recommends improvements
- `ReviewCoordinatorAgent`: Orchestrates the review process and aggregates findings

**Example Usage**:
```python
from vaahai.agents.factory import AgentFactory
from vaahai.agents.group_chat import ReviewGroupChatManager

# Create specialized agents
agent_factory = AgentFactory(llm_provider)
language_detector = agent_factory.create_agent("language_detector")
framework_detector = agent_factory.create_agent("framework_detector")
standards_analyzer = agent_factory.create_agent("standards_analyzer")
security_auditor = agent_factory.create_agent("security_auditor")
coordinator = agent_factory.create_agent("review_coordinator")

# Set up group chat
group_chat = ReviewGroupChatManager(
    agents=[language_detector, framework_detector, standards_analyzer, security_auditor],
    coordinator=coordinator
)

# Run collaborative review
review_result = group_chat.run_review(file_info, static_analysis_results)
```

#### Output Formatting

The Output Formatting component formats review results for presentation.

**Implementation Details**:
- Supports multiple output formats (terminal, Markdown, HTML)
- Applies consistent styling and structure
- Handles code syntax highlighting
- Manages output to console or file

**Key Classes**:
- `FormatterRegistry`: Manages available formatters
- `Formatter`: Abstract base class for formatters
- `TerminalFormatter`, `MarkdownFormatter`, `HTMLFormatter`: Specific formatter implementations
- `FormattedOutput`: Representation of formatted output

**Example Usage**:
```python
from vaahai.formatters import FormatterRegistry

registry = FormatterRegistry()
formatter = registry.get_formatter("terminal")
output = formatter.format(review_result)

if output_file:
    with open(output_file, "w") as f:
        f.write(output.content)
else:
    print(output.content)
```

### External Integrations

#### LLM Providers

The LLM Providers component interfaces with different LLM services.

**Implementation Details**:
- Supports multiple providers (OpenAI, Ollama)
- Handles authentication and API communication
- Manages rate limiting and error handling
- Optimizes token usage and costs
- Provides consistent interface across providers

**Key Classes**:
- `LLMProviderFactory`: Creates appropriate provider instances
- `LLMProvider`: Abstract base class for providers
- `OpenAIProvider`, `OllamaProvider`: Specific provider implementations
- `LLMResponse`: Normalized representation of LLM responses

**Example Usage**:
```python
from vaahai.llm.providers import LLMProviderFactory

provider = LLMProviderFactory.create("openai", api_key="sk-...")
response = provider.complete(
    prompt="Review this code: def example(): pass",
    max_tokens=1000,
    temperature=0.7
)

print(response.content)
```

#### Static Analysis Tools

Vaahai integrates with external static analysis tools through adapters.

**Implementation Details**:
- Runs tools as subprocesses or through APIs
- Parses tool-specific output formats
- Handles tool-specific configuration
- Manages tool dependencies and availability

**Key Tools**:
- **Python**: pylint, flake8, bandit, mypy
- **JavaScript**: ESLint, JSHint
- **General**: SonarQube, CodeQL

## Data Flow

### Review Process Flow

1. **User Initiates Review**:
   - User runs `vaahai review [path]` command
   - CLI parses arguments and options
   - Configuration is loaded and validated

2. **File Scanning**:
   - Code Scanner identifies relevant files
   - Files are filtered based on inclusion/exclusion rules
   - File metadata and content are extracted

3. **Static Analysis**:
   - Appropriate analyzers are selected for each file
   - Analyzers run and produce raw results
   - Results are parsed and normalized
   - Results are aggregated across tools

4. **Multi-Agent Review**:
   - Review Orchestrator initializes the Autogen multi-agent system
   - Specialized agents are created and configured
   - Code and static analysis results are provided to agents
   - Agents collaborate through GroupChat to analyze the code
   - Review Coordinator manages the conversation and aggregates findings

5. **Agent Collaboration Flow**:
   - Language Detector Agent identifies programming languages and features
   - Framework Detector Agent identifies frameworks and architectural patterns
   - Standards Analyzer Agent evaluates adherence to coding standards
   - Security Auditor Agent identifies security vulnerabilities
   - Review Coordinator Agent orchestrates the process and builds consensus
   - Agents communicate and refine their analysis through structured dialogue

6. **Result Processing**:
   - Agent findings are structured into review results
   - Issues are categorized and prioritized
   - Suggested fixes are extracted
   - Results are merged with static analysis findings

7. **Output Generation**:
   - Appropriate formatter is selected based on user preference
   - Results are formatted for presentation
   - Output is displayed or saved to file

### Key Data Models

1. **Input Models**:
   - `FileInfo`: File metadata and content
   - `AnalysisResult`: Static analysis findings
   - `AgentConfig`: Configuration for specialized agents

2. **Processing Models**:
   - `AgentMessage`: Communication between agents
   - `ReviewContext`: Context provided to agents
   - `AgentFinding`: Individual agent analysis results

3. **Output Models**:
   - `ReviewIssue`: Identified code issues
   - `ReviewSuggestion`: Suggested improvements
   - `ReviewResult`: Complete review output

## Implementation Details

### Key Interfaces

1. **Agent Interface**:
   - `Agent`: Abstract base class for agents
   - `AgentFactory`: Creates specialized agents based on configuration

2. **LLM Provider Interface**:
   - `LLMProvider`: Abstract base class for providers
   - `LLMProviderFactory`: Creates appropriate provider instances

3. **Formatter Interface**:
   - `Formatter`: Abstract base class for formatters
   - `FormatterRegistry`: Manages available formatters

### Data Structures

#### FileInfo

```python
class FileInfo:
    path: str                # Absolute path to file
    relative_path: str       # Path relative to project root
    language: str            # Detected programming language
    size: int                # File size in bytes
    content: str             # File content
    encoding: str            # File encoding
```

#### AnalysisResult

```python
class AnalysisResult:
    tool: str                # Name of analysis tool
    file_path: str           # Path to analyzed file
    line: int                # Line number of finding
    column: int              # Column number of finding
    severity: str            # Severity level (high, medium, low, info)
    rule_id: str             # Identifier of violated rule
    message: str             # Description of the issue
    fix: Optional[str]       # Suggested fix if available
```

#### AgentConfig

```python
class AgentConfig:
    agent_type: str          # Type of agent (language_detector, security_auditor, etc.)
    model: str               # LLM model to use
    temperature: float       # Temperature for generation
    max_tokens: int          # Maximum tokens for response
    system_prompt: str       # System prompt for the agent
    user_prompt_template: str # Template for user prompts
```

#### ReviewResult

```python
class ReviewResult:
    summary: str             # Overall summary of review
    issues: List[ReviewIssue] # Identified issues
    suggestions: List[ReviewSuggestion] # Suggested improvements
    metrics: Dict[str, Any]  # Review metrics
    static_analysis: List[AnalysisResult] # Static analysis results
    agent_findings: Dict[str, List[AgentFinding]] # Raw agent findings
```

## Configuration

1. **File Locations**:
   - Source code in `vaahai/` directory
   - Tests in `tests/` directory
   - Documentation in `docs/` directory

2. **Dependencies**:
   - Core Python libraries
   - Typer for CLI
   - Pydantic for data validation
   - Microsoft Autogen for multi-agent system
   - Various static analysis tools

3. **Configuration**:
   - User-level configuration in `~/.config/vaahai/config.toml`
   - Project-level configuration in `.vaahai.toml`
   - Environment variables with `VAAHAI_` prefix
   - Agent configuration in `.vaahai/agents/` directory

## Extension Points

Vaahai provides several extension points for customization:

1. **Static Analyzers**: Add new analyzers by implementing the `Analyzer` interface
2. **LLM Providers**: Add new providers by implementing the `LLMProvider` interface
3. **Formatters**: Add new output formats by implementing the `Formatter` interface
4. **Agents**: Add new specialized agents by extending the agent system
5. **Commands**: Add new CLI commands by extending the Typer application

## Security Considerations

1. **API Key Management**:
   - API keys stored securely using environment variables or secure storage
   - Keys never logged or exposed in outputs
   - Support for credential providers and rotation

2. **Code Privacy**:
   - Options for local LLM usage to avoid sending code externally
   - Clear documentation on what is sent to external services
   - No persistent storage of code by default

3. **Dependency Security**:
   - Regular updates of dependencies
   - Vulnerability scanning in CI/CD pipeline
   - Minimal dependency footprint

4. **Input Validation**:
   - Validation of all user inputs
   - Protection against path traversal and injection
   - Secure handling of file operations

## Performance Considerations

1. **Large Codebase Handling**:
   - Efficient file filtering to focus on relevant files
   - Parallel processing of multiple files
   - Chunking strategies for large files
   - Progress reporting for long-running operations

2. **Token Optimization**:
   - Smart chunking to maximize LLM context usage
   - Prioritization of relevant code sections
   - Compression techniques for context
   - Caching of similar requests

3. **Response Time**:
   - Asynchronous processing where appropriate
   - Background processing for non-blocking operations
   - Timeout handling for external services
   - Performance metrics and optimization

## Development Environment

1. **Required Tools**:
   - Python 3.9+
   - Poetry for dependency management
   - Git for version control
   - pytest for testing
   - pre-commit for quality checks

2. **Setup Process**:
   ```bash
   # Clone repository
   git clone https://github.com/webreinvent/vaahai.git
   cd vaahai
   
   # Install dependencies
   poetry install
   
   # Set up pre-commit hooks
   poetry run pre-commit install
   
   # Run tests
   poetry run pytest
   ```

3. **Development Workflow**:
   - Create feature branch from main
   - Implement changes with tests
   - Run quality checks and tests
   - Submit pull request
   - Code review and approval
   - Merge to main

## Deployment

1. **Package Distribution**:
   - Published to PyPI
   - Installable via pip or poetry
   - Docker image for containerized usage

2. **Installation**:
   ```bash
   # From PyPI
   pip install vaahai
   
   # From source
   git clone https://github.com/webreinvent/vaahai.git
   cd vaahai
   pip install .
   ```

3. **Configuration**:
   - User-level configuration in `~/.config/vaahai/config.toml`
   - Project-level configuration in `.vaahai.toml`
   - Environment variables with `VAAHAI_` prefix

## Conclusion

This architecture provides a solid foundation for implementing Vaahai as a modular, extensible, and maintainable system. The component-based design allows for incremental development and easy extension to support additional languages, tools, and features in the future.
