# Vaahai: AI-Augmented Code Review Tool

## Product Requirements Document - Technical Specifications

**Version:** 1.0.0  
**Date:** June 1, 2025  
**Status:** Draft  

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Specifications](#component-specifications)
3. [Data Flow](#data-flow)
4. [API Specifications](#api-specifications)
5. [Technology Stack](#technology-stack)
6. [Integration Points](#integration-points)
7. [Development Environment](#development-environment)
8. [Testing Strategy](#testing-strategy)

## Architecture Overview

Vaahai follows a modular, component-based architecture designed for extensibility and maintainability. The system is structured around a core CLI application that orchestrates interactions between specialized components.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLI Application                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Manager                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌──────────────┬───────────────┴────────────────┬─────────────────┐
│              │                                 │                 │
▼              ▼                                 ▼                 ▼
┌──────────┐  ┌─────────────┐  ┌──────────────────┐  ┌────────────┐
│Code      │  │Static       │  │Agent             │  │Output      │
│Scanner   │  │Analysis     │  │Orchestration     │  │Formatting  │
│          │  │Integration  │  │                  │  │            │
└──────┬───┘  └──────┬──────┘  └────────┬─────────┘  └─────┬──────┘
       │              │                  │                  │
       └──────────────┼──────────────────┼──────────────────┘
                      │                  │
                      ▼                  ▼
              ┌───────────────┐  ┌───────────────┐
              │Static Analysis│  │LLM            │
              │Tools          │  │Providers      │
              └───────────────┘  └───────────────┘
```

### Key Architectural Principles

1. **Separation of Concerns**: Each component has a well-defined responsibility and interface
2. **Dependency Injection**: Components receive their dependencies rather than creating them
3. **Extensibility**: Abstract base classes and factory patterns enable easy extension
4. **Configuration-Driven**: Behavior can be customized through configuration rather than code changes
5. **Fail Gracefully**: Components handle errors and provide meaningful feedback

## Component Specifications

### CLI Application

The entry point for the application, responsible for parsing command-line arguments, initializing components, and coordinating the review process.

**Responsibilities**:
- Parse command-line arguments
- Initialize and configure components
- Coordinate the review workflow
- Handle user interaction
- Manage error reporting

**Interfaces**:
- Command-line interface following Typer conventions
- Component initialization and configuration API

**Dependencies**:
- Configuration Manager
- Code Scanner
- Agent Orchestration
- Output Formatting

### Configuration Manager

Manages application settings from multiple sources with appropriate precedence.

**Responsibilities**:
- Load configuration from files
- Merge configuration from multiple sources
- Validate configuration values
- Provide access to configuration settings
- Secure storage of sensitive information

**Interfaces**:
- Configuration loading and saving API
- Configuration access API

**Dependencies**:
- None

### Code Scanner

Identifies and processes code files for review.

**Responsibilities**:
- Identify files matching specified patterns
- Filter files based on inclusion/exclusion rules
- Extract file metadata
- Read file contents
- Handle large files and directories

**Interfaces**:
- File scanning API
- File content access API

**Dependencies**:
- Configuration Manager

### Static Analysis Integration

Runs static analysis tools and processes their results.

**Responsibilities**:
- Detect available static analysis tools
- Run appropriate tools for each file type
- Parse tool outputs into standardized format
- Aggregate results from multiple tools
- Handle tool-specific configuration

**Interfaces**:
- Analyzer registry and factory
- Analysis execution API
- Result processing API

**Dependencies**:
- Configuration Manager
- External static analysis tools

### Agent Orchestration

Manages LLM agents using the AutoGen framework to generate code reviews.

**Responsibilities**:
- Initialize and configure AutoGen agents
- Prepare prompts with code and static analysis context
- Manage agent interactions
- Process agent outputs
- Handle token limitations and chunking

**Interfaces**:
- Agent initialization API
- Review generation API
- Result processing API

**Dependencies**:
- Configuration Manager
- LLM Providers
- Microsoft AutoGen framework

### Output Formatting

Formats review results for presentation in different formats.

**Responsibilities**:
- Format review results for terminal display
- Generate Markdown documentation
- Create HTML reports
- Apply consistent styling and structure
- Handle code syntax highlighting

**Interfaces**:
- Formatter registry and factory
- Format generation API
- Output writing API

**Dependencies**:
- Configuration Manager

### LLM Providers

Interfaces with different LLM services to generate code reviews.

**Responsibilities**:
- Authenticate with LLM services
- Send prompts and receive responses
- Handle rate limiting and errors
- Manage token usage
- Implement provider-specific optimizations

**Interfaces**:
- Provider registry and factory
- LLM interaction API

**Dependencies**:
- Configuration Manager
- External LLM services (OpenAI, Ollama)

## Data Flow

The following diagram illustrates the data flow through the system during a typical code review operation:

```
┌──────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│          │     │           │     │           │     │           │
│  Input   │────▶│  Scanner  │────▶│  Files    │────▶│ Analyzers │
│          │     │           │     │           │     │           │
└──────────┘     └───────────┘     └───────────┘     └─────┬─────┘
                                                           │
                                                           ▼
┌──────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
│          │     │           │     │           │     │           │
│ Formatter│◀────│  Results  │◀────│  Agents   │◀────│ Analysis  │
│          │     │           │     │           │     │ Results   │
└─────┬────┘     └───────────┘     └───────────┘     └───────────┘
      │                                  ▲
      │                                  │
      │                            ┌───────────┐
      │                            │           │
      │                            │   LLM     │
      │                            │ Providers │
      │                            │           │
      │                            └───────────┘
      ▼
┌──────────┐
│          │
│  Output  │
│          │
└──────────┘
```

### Data Flow Steps

1. **Input Processing**:
   - User provides command-line input
   - CLI parses arguments and options
   - Configuration is loaded and merged

2. **File Scanning**:
   - Scanner identifies files matching criteria
   - File metadata is extracted
   - File contents are read

3. **Static Analysis**:
   - Appropriate analyzers are selected for each file
   - Analyzers run and produce raw results
   - Results are parsed and normalized
   - Results are aggregated across tools

4. **Review Generation**:
   - Code context and analysis results are prepared
   - Prompts are constructed for LLM
   - Agents are initialized with appropriate configuration
   - LLM generates review content
   - Review content is parsed and structured

5. **Output Generation**:
   - Appropriate formatter is selected
   - Review is formatted according to output type
   - Output is presented to user or saved to file

## API Specifications

### CLI API

The command-line interface follows the Typer convention with commands, subcommands, and options.

**Main Command**:
```
vaahai [OPTIONS] COMMAND [ARGS]...
```

**Global Options**:
- `--verbose / -v`: Enable verbose output
- `--config PATH`: Path to custom config file
- `--output-format [terminal|markdown|html]`: Output format for results

**Subcommands**:
- `review`: Perform code review
- `config`: Manage configuration
- `analyze`: Run static analysis only

### Component APIs

#### Configuration Manager API

```python
class ConfigManager:
    def load(self, paths: List[Path]) -> None:
        """Load configuration from specified paths"""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        
    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to specified path"""
```

#### Code Scanner API

```python
class CodeScanner:
    def scan(self, path: Path, patterns: List[str], exclusions: List[str]) -> List[CodeFile]:
        """Scan for files matching criteria"""
        
    def read_file(self, file: CodeFile) -> str:
        """Read file contents"""
```

#### Static Analysis API

```python
class AnalyzerFactory:
    def get_analyzer(self, language: str, analyzer_name: str) -> BaseAnalyzer:
        """Get analyzer instance for language and name"""
        
class BaseAnalyzer:
    def analyze(self, file_path: Path) -> str:
        """Run analysis on file"""
        
    def parse_results(self, raw_results: str) -> List[Issue]:
        """Parse raw results into structured format"""
```

#### Agent Orchestration API

```python
class ReviewOrchestrator:
    def generate_review(self, code: str, static_analysis_results: str, context: str, language: str) -> Review:
        """Generate code review using agents"""
        
    def extract_suggestions(self, review: Review) -> List[Suggestion]:
        """Extract actionable suggestions from review"""
```

#### Output Formatting API

```python
class FormatterFactory:
    def get_formatter(self, format_type: str) -> BaseFormatter:
        """Get formatter instance for format type"""
        
class BaseFormatter:
    def format_review(self, review: Review) -> str:
        """Format review for output"""
        
    def save(self, formatted_review: str, output_path: Path) -> None:
        """Save formatted review to file"""
```

#### LLM Provider API

```python
class ProviderFactory:
    def get_provider(self, provider_name: str) -> BaseLLMProvider:
        """Get LLM provider instance"""
        
class BaseLLMProvider:
    def initialize(self) -> None:
        """Initialize provider with configuration"""
        
    def generate(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate response from LLM"""
```

## Technology Stack

### Core Technologies

| Component | Technology | Justification |
|-----------|------------|---------------|
| Programming Language | Python 3.9+ | Rich ecosystem, strong typing support, widespread adoption |
| CLI Framework | Typer | Modern, type-annotated interface with automatic help generation |
| Configuration | TOML | Human-readable, structured format with strong typing |
| Dependency Management | Poetry | Modern dependency management with lock files and virtual environments |

### External Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| typer | ^0.9.0 | CLI framework |
| rich | ^13.4.0 | Terminal formatting and display |
| pydantic | ^2.0.0 | Data validation and settings management |
| tomli | ^2.0.0 | TOML parsing |
| autogen | ^0.2.0 | LLM agent orchestration |
| openai | ^1.0.0 | OpenAI API client |
| requests | ^2.30.0 | HTTP client for API interactions |
| markdown | ^3.4.0 | Markdown generation |
| jinja2 | ^3.1.0 | HTML template rendering |
| pygments | ^2.15.0 | Code syntax highlighting |

### Development Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| pytest | ^7.3.0 | Testing framework |
| black | ^23.3.0 | Code formatting |
| isort | ^5.12.0 | Import sorting |
| mypy | ^1.3.0 | Static type checking |
| pylint | ^2.17.0 | Static code analysis |
| pytest-cov | ^4.1.0 | Test coverage |
| pre-commit | ^3.3.0 | Git hooks for quality checks |

## Integration Points

### Static Analysis Tools

Vaahai integrates with various static analysis tools through command-line execution and result parsing.

**Python Tools**:
- pylint: General Python linting
- flake8: Style guide enforcement
- bandit: Security vulnerability scanning
- mypy: Type checking

**PHP Tools**:
- phpcs: PHP CodeSniffer
- phpstan: Static analysis
- psalm: Static analysis and type checking

**JavaScript/Vue Tools**:
- eslint: Linting and style checking
- jshint: JavaScript code quality

### LLM Providers

Vaahai integrates with LLM providers through their APIs or local interfaces.

**OpenAI**:
- API-based integration
- Support for GPT-4 and GPT-3.5 models
- Authentication via API key

**Ollama**:
- Local HTTP API integration
- Support for various open-source models
- Configuration via host and port settings

### Version Control Systems

While not directly integrated in the MVP, future versions will support:

- Git: Diff generation, commit analysis
- GitHub/GitLab: PR/MR integration, comment generation

## Development Environment

### Requirements

- Python 3.9+
- Poetry for dependency management
- Git for version control
- Access to LLM services (OpenAI API key or Ollama installation)
- Static analysis tools for development language

### Setup Process

1. Clone repository
2. Install Poetry
3. Install dependencies with `poetry install`
4. Configure pre-commit hooks with `pre-commit install`
5. Set up environment variables for API keys

### Development Workflow

1. Create feature branch from main
2. Implement changes with tests
3. Run linting and type checking
4. Run tests with coverage
5. Submit pull request
6. Code review and approval
7. Merge to main

## Testing Strategy

### Test Levels

1. **Unit Tests**:
   - Component-level testing with mocked dependencies
   - Focus on business logic and edge cases
   - High coverage target (90%+)

2. **Integration Tests**:
   - Testing component interactions
   - Mock external services (LLMs, static analyzers)
   - Focus on data flow and error handling

3. **System Tests**:
   - End-to-end testing of main workflows
   - Limited scope due to external dependencies
   - Focus on user experience and output quality

4. **Performance Tests**:
   - Response time for various file sizes
   - Memory usage for large codebases
   - Token usage optimization

### Test Automation

- CI pipeline for automated testing on pull requests
- Pre-commit hooks for local quality checks
- Regular scheduled runs against benchmark codebases

### Test Data

- Synthetic code samples with known issues
- Open-source repositories for real-world testing
- Benchmark suite for performance comparison
