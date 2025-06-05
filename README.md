# VaahAI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

**VaahAI** is a multi-agent AI CLI tool built with Microsoft's Autogen Framework, designed to enhance code quality and development workflows through AI-powered code review, auditing, generation, and scaffolding capabilities.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized AI agents collaborate to perform complex tasks
- **Code Review**: Comprehensive code review focusing on quality, style, and best practices
- **Code Audit**: Security vulnerability detection, compliance checking, and architectural assessment
- **Code Generation**: AI-powered code generation from natural language descriptions
- **Multiple LLM Support**: OpenAI, Claude, Junie, and local models via Ollama
- **Flexible Configuration**: Layered configuration system with global defaults and project-specific settings
- **Git Integration**: Commit applied changes, generate meaningful commit messages, and prepare pull requests

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation) (Python package manager)
- Git
- Docker (optional, for code execution)

### Installation

```bash
# Clone the repository
git clone https://github.com/webreinvent/vaahai.git
cd vaahai

# Install dependencies with Poetry
poetry install

# Activate the Poetry virtual environment
poetry shell
```

### Development Setup

```bash
# Install development dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Format code
poetry run black vaahai
poetry run isort vaahai

# Lint code
poetry run flake8 vaahai
poetry run mypy vaahai
```

### Configuration

```bash
# Run the configuration wizard
poetry run vaahai config init

# Or manually edit the configuration file
nano ~/.vaahai/config.toml
```

## 🛠️ Usage

### CLI Command Structure

VaahAI provides a modular CLI with the following main commands:

- `vaahai helloworld`: Test command to verify proper functioning
- `vaahai config`: Configuration management commands
  - `vaahai config init`: Set up initial configuration
  - `vaahai config show`: Display current configuration
- `vaahai review`: Code review commands
  - `vaahai review run`: Run a code review on specified path
- `vaahai audit`: Security and compliance audit commands
  - `vaahai audit run`: Run a security/compliance audit on specified path
- `vaahai version`: Display version information
  - `vaahai version show`: Show current VaahAI version

Each command supports the `--help` flag for detailed usage information.

### Basic Commands

```bash
# Test installation and configuration
poetry run vaahai helloworld run

# Review code in a file or directory
poetry run vaahai review run --path ./my_project --depth standard

# Audit a project for security and compliance
poetry run vaahai audit run --path ./my_project --security --compliance owasp

# Show version information
poetry run vaahai version show
```

### Example Workflow

```bash
# Review a Python file
poetry run vaahai review run --path ./app.py --focus quality

# Apply suggested changes
poetry run vaahai apply --file review_suggestions.json

# Commit the changes
poetry run vaahai commit --message "Fix code quality issues in app.py"
```

## 🏗️ Project Structure

```
vaahai/
├── ai_docs/         # AI-specific documentation
├── ai_prompts/      # Prompt templates for AI agents
├── docs/            # User and developer documentation
├── specs/           # Project specifications and requirements
├── vaahai/          # Main package
│   ├── agents/      # Agent implementations
│   ├── cli/         # CLI commands and handlers
│   │   ├── commands/  # Command implementations
│   │   │   ├── audit/     # Audit command
│   │   │   ├── config/    # Configuration command
│   │   │   ├── helloworld/  # Hello world test command
│   │   │   ├── review/    # Code review command
│   │   │   └── version/   # Version command
│   │   └── utils/     # CLI utilities
│   ├── config/      # Configuration management
│   ├── llm/         # LLM provider integrations
│   └── utils/       # Utility functions and helpers
└── tests/           # Test suite
```

## 📝 Documentation

For more detailed documentation, please refer to:

- [Project Plan](/specs/PROJECT_PLAN.md)
- [Features Specification](/specs/FEATURES.md)
- [Technical Architecture](/specs/TECHNICAL_ARCHITECTURE.md)
- [User Guide](/docs/USER_GUIDE.md)
- [API Reference](/docs/API_REFERENCE.md)

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to get involved.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Microsoft Autogen Framework](https://github.com/microsoft/autogen)
- [Typer](https://typer.tiangolo.com/)
- [InquirerPy](https://github.com/kazhala/InquirerPy)
- All our contributors and supporters
