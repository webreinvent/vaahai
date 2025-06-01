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

#### Static Analysis Integration

The Static Analysis Integration component runs static analysis tools and processes their results.

**Implementation Details**:
- Detects available static analysis tools
- Selects appropriate analyzers based on file type
- Runs analyzers with appropriate configuration
- Parses and normalizes analyzer outputs
- Aggregates results from multiple analyzers

**Key Classes**:
- `AnalyzerRegistry`: Manages available analyzers
- `Analyzer`: Abstract base class for analyzers
- `PylintAnalyzer`, `Flake8Analyzer`, etc.: Specific analyzer implementations
- `AnalysisResult`: Normalized representation of analysis findings

**Example Usage**:
```python
from vaahai.core.analyzer import AnalyzerRegistry, AnalysisResult

registry = AnalyzerRegistry()
analyzer = registry.get_analyzer_for_language("python")
results = analyzer.analyze("path/to/file.py")

for result in results:
    print(f"{result.severity}: {result.message} at line {result.line}")
```

#### Agent Orchestration

The Agent Orchestration component manages LLM agents to generate code reviews.

**Implementation Details**:
- Initializes and configures AutoGen agents
- Prepares prompts with code and context
- Manages agent interactions
- Processes and structures agent outputs
- Handles token limitations through chunking

**Key Classes**:
- `AgentOrchestrator`: Coordinates agent interactions
- `PromptBuilder`: Constructs prompts for agents
- `ReviewAgent`, `AssistantAgent`: Specialized agents for review tasks
- `ReviewResult`: Structured representation of review output

**Example Usage**:
```python
from vaahai.core.orchestrator import AgentOrchestrator
from vaahai.llm.providers import LLMProviderFactory

provider = LLMProviderFactory.create("openai")
orchestrator = AgentOrchestrator(provider)

review_result = orchestrator.review_code(
    code="def example(): pass",
    language="python",
    static_analysis_results=analysis_results,
    review_depth="standard"
)

print(review_result.summary)
for issue in review_result.issues:
    print(f"{issue.severity}: {issue.message} at line {issue.line}")
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

4. **LLM Review**:
   - Prompt is constructed with code and static analysis results
   - LLM provider is initialized with appropriate configuration
   - Prompt is sent to LLM for processing
   - Response is received and parsed

5. **Result Processing**:
   - LLM response is structured into review results
   - Issues are categorized and prioritized
   - Suggested fixes are extracted
   - Results are merged with static analysis findings

6. **Output Generation**:
   - Appropriate formatter is selected based on user preference
   - Results are formatted for presentation
   - Output is displayed or saved to file

7. **Interactive Fix Application** (if enabled):
   - Suggested fixes are presented to user
   - User selects fixes to apply
   - Selected fixes are applied to original files

### Data Models

#### File Information

```python
class FileInfo:
    path: str                # Absolute path to file
    relative_path: str       # Path relative to project root
    language: str            # Detected programming language
    size: int                # File size in bytes
    content: str             # File content
    encoding: str            # File encoding
    line_count: int          # Number of lines
```

#### Analysis Result

```python
class AnalysisResult:
    tool: str                # Name of the analysis tool
    file_path: str           # Path to the analyzed file
    line: int                # Line number
    column: int              # Column number
    severity: str            # Severity level (critical, error, warning, info)
    code: str                # Issue code or ID
    message: str             # Description of the issue
    suggestion: Optional[str] # Suggested fix
```

#### Review Issue

```python
class ReviewIssue:
    file_path: str           # Path to the file
    line: int                # Line number
    column: Optional[int]    # Column number
    severity: str            # Severity (critical, important, minor)
    category: str            # Issue category (bug, security, performance, style)
    message: str             # Description of the issue
    explanation: str         # Detailed explanation
    suggestion: Optional[str] # Suggested fix
    source: str              # Source (llm, static_analysis)
```

#### Review Result

```python
class ReviewResult:
    file_path: str           # Path to the reviewed file
    language: str            # Programming language
    summary: str             # Overall summary
    strengths: List[str]     # Identified strengths
    issues: List[ReviewIssue] # Identified issues
    suggestions: List[str]   # General suggestions
    metrics: Dict[str, Any]  # Review metrics
```

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

## Extensibility

The architecture is designed for extensibility in several dimensions:

1. **Language Support**:
   - Abstract language detection and handling
   - Pluggable language-specific analyzers
   - Language-specific prompt engineering

2. **LLM Providers**:
   - Provider interface abstraction
   - Pluggable provider implementations
   - Consistent handling across providers

3. **Output Formats**:
   - Formatter registry and factory pattern
   - Pluggable formatter implementations
   - Consistent output structure

4. **Static Analyzers**:
   - Analyzer registry and factory pattern
   - Pluggable analyzer implementations
   - Normalized result format

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
