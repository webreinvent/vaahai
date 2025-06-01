# Project Structure

This document provides detailed information about the Vaahai project structure, code organization, and technical implementation details.

## Directory Structure

The project is organized into several key directories:

### `/vaahai/core`

Contains core functionality of the application, including:

- **Configuration System**: A modular configuration system using the singleton pattern
  - `config/` - Package with specialized modules for configuration management
  - `config/models.py` - Pydantic data models for configuration
  - `config/validation.py` - Configuration validation logic
  - `config/migration.py` - Schema versioning and migration
  - `config/manager.py` - ConfigManager with singleton implementation

```python
# Using the configuration system
from vaahai.core.config import config_manager

# Get a configuration value
api_key = config_manager.get("llm.api_key")

# Set a configuration value
config_manager.set("review.depth", "thorough")
```

- **Code Scanner**: A robust file scanning and filtering system
  - `scanner/` - Package with modules for code scanning and filtering
  - `scanner/scanner.py` - CodeScanner implementation with singleton pattern
  - `scanner/filters.py` - Filter classes for file selection
  - `scanner/__init__.py` - Package exports and singleton instance

```python
# Using the code scanner
from vaahai.core.scanner import code_scanner

# Scan a directory with filters
code_scanner.set_include_extensions(["py", "js"])
code_scanner.set_exclude_patterns(["*_test.py"])
files = code_scanner.scan_path("/path/to/project")

# Process scanned files
for file_info in files:
    print(f"{file_info.path} - {file_info.language} - {file_info.size} bytes")
```

### `/vaahai/cli`

Contains the command-line interface implementation:

- `commands/` - Individual command implementations
- `utils.py` - CLI utility functions
- `main.py` - CLI entry point and command registration

### `/vaahai/providers`

Contains implementations for different LLM providers:

- `base.py` - Base provider interface
- `openai.py` - OpenAI provider implementation
- `ollama.py` - Ollama provider implementation

### `/docs`

Contains user-facing documentation, guides, and tutorials for human readers. This includes installation instructions, usage examples, and API documentation.

### `/ai_docs`

Contains AI-specific documentation formatted for AI tools to better understand the codebase. This documentation is more detailed and structured specifically to help AI systems comprehend the architecture, design patterns, and business logic.

### `/specs`

Contains technical specifications, requirements documents, and design proposals for the project. These documents outline the planned functionality and implementation details.

### `/.claude`

Contains configuration files and prompts for Claude AI integration, including specialized commands and templates for AI-assisted code review.

```bash
# Directory structure
.claude/
└── commands/
    ├── code_review.prompt        # General code review template
    ├── fix_suggestion.prompt     # Fix generation template
    ├── performance_optimization.prompt  # Performance-focused review
    └── security_audit.prompt     # Security-focused review
```

## Design Patterns

Vaahai uses several key design patterns throughout the codebase:

### Singleton Pattern

Used for components that should maintain a single state throughout the application lifecycle:

- `ConfigManager` - Manages configuration state
- `CodeScanner` - Manages scanning state and filters

### Factory Pattern

Used for creating provider instances:

- `LLMProviderFactory` - Creates appropriate LLM provider instances based on configuration

### Strategy Pattern

Used for interchangeable algorithms:

- `OutputFormatter` - Different formatting strategies (terminal, markdown, HTML)
- `FileFilter` - Different filtering strategies for file selection

### Command Pattern

Used for CLI commands:

- Each command in the `commands/` directory implements a common interface

## Component Interactions

The following diagram illustrates how the major components interact:

```
CLI Commands → ConfigManager → CodeScanner → LLM Providers → Output Formatters
```

1. CLI commands parse user input and options
2. Configuration is loaded from ConfigManager
3. CodeScanner identifies and filters relevant files
4. LLM Providers process code for review
5. Output Formatters present results to the user

## Testing Strategy

The project uses pytest for testing with the following organization:

- Unit tests for individual components
- Integration tests for component interactions
- End-to-end tests for CLI commands

## Development Guidelines

When contributing to the codebase:

1. Follow the established patterns for each component
2. Maintain backward compatibility where possible
3. Add appropriate tests for new functionality
4. Update documentation to reflect changes

For more detailed information about specific components, see their respective documentation files.
