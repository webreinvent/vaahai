# Vaahai

Agentic Coding, Review, Audit and Generation

## Overview

Vaahai is an AI-augmented code review CLI tool that combines static analysis with LLM capabilities to provide comprehensive code reviews, suggestions, and automated fixes.

## Installation

```bash
# Install from PyPI
pip install vaahai

# Verify installation
vaahai --version
```

## Quick Start

```bash
# Set up your configuration
vaahai config init

# Review a single file
vaahai review path/to/file.py

# Review a directory recursively
vaahai review src/

# Review with specific include/exclude patterns
vaahai review src/ --include="*.py" --exclude="*_test.py"

# Review with specific focus and depth
vaahai review important_module.py --depth thorough --focus security
```

## Features

- **Code Scanning**: Scan directories with customizable filters for file extensions, patterns, and content
- **Static Analysis**: Integrate with static analysis tools for code quality checks
- **LLM Integration**: Leverage LLMs for contextual code review and suggestions
- **Interactive Fixes**: Apply suggested fixes interactively
- **Multiple Output Formats**: Generate reports in terminal, markdown, or HTML formats

## Implementation Status

| Feature | Status | Description |
|---------|--------|-------------|
| ✅ Configuration Manager | Complete | Configuration loading and validation |
| ✅ CLI Application | Complete | Command-line interface |
| ✅ Code Scanner | Complete | File scanning and processing |
| ✅ CLI Command Simplification | Complete | Simplified command structure |
| ⏳ Output Formatting | Deprioritized | Being replaced by Autogen Framework |
| 🔄 Autogen Framework Integration | In Progress | Multi-agent system for code review with Docker-based code execution |
| 🔄 Hello World Agent MVP | In Progress | Simple agent to validate Autogen integration framework |
| ⏳ Static Analysis | Planned | Integration with static analysis tools |
| ⏳ LLM Provider Interface | Planned | Support for multiple LLM providers |
| ⏳ Review Orchestration | Planned | Manage the review process |
| ⏳ Fix Suggestion | Planned | Suggest code improvements |

For detailed implementation status, see the [Implementation Status](/specs/implementation/implementation_status.md) documentation.
For the complete development roadmap, see the [Implementation Roadmap](/specs/implementation/implementation_roadmap.md).

## Available Commands

### `review`

Review code files with customizable filters and analysis.

```bash
vaahai review [PATH] [OPTIONS]
```

**Arguments:**
- `PATH`: Path to file or directory to review (required)

**Options:**
- `--depth {quick,standard,thorough}`: Review depth (default: standard)
- `--focus {all,security,performance,style}`: Focus area (default: all)
- `--output {terminal,markdown,html}`: Output format (default: terminal)
- `--output-file FILE`: Save output to a file
- `--include PATTERN`: Patterns to include (can be used multiple times)
- `--exclude PATTERN`: Patterns to exclude (can be used multiple times)
- `--max-file-size SIZE`: Maximum file size in bytes (default: 1MB)
- `--interactive`: Enable interactive fix application
- `--save-history`: Save review results to history
- `--private`: Use only local resources

### `config`

Manage Vaahai configuration.

```bash
vaahai config [ACTION] [OPTIONS]
```

**Actions:**
- `init`: Initialize configuration
- `get KEY`: Get a configuration value
- `set KEY VALUE`: Set a configuration value
- `list`: List all configuration values
- `reset`: Reset configuration to defaults
- `locations`: Show configuration file locations

**Options:**
- `--global`: Apply to global configuration
- `--local`: Apply to local configuration
- `--env`: Show environment variable override

### `analyze`

Run static analysis on code files.

```bash
vaahai analyze [PATH] [OPTIONS]
```

**Arguments:**
- `PATH`: Path to file or directory to analyze

**Options:**
- `--analyzer {pylint,eslint,all}`: Analyzer to use
- `--format {text,json,html}`: Output format
- `--output-file FILE`: Save output to a file

## Documentation

Comprehensive documentation is available in the `/docs` directory:

- [Installation Guide](docs/installation.md)
- [Getting Started](docs/getting_started.md)
- [Usage Guide](docs/usage.md)
- [Commands Reference](docs/commands.md)
- [Configuration Guide](docs/configuration.md)
- [Code Scanner](docs/scanner.md)

To view the documentation in your browser:

```bash
# Install Docsify (if not already installed)
npm install -g docsify-cli

# Start the documentation server
docsify serve docs

# Access at http://localhost:3000
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
