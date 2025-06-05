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

### Basic Commands

```bash
# Test installation and configuration
poetry run vaahai helloworld

# Review code in a file or directory
poetry run vaahai review --path ./my_project --depth standard

# Audit a project for security and compliance
poetry run vaahai audit --path ./my_project --security --compliance owasp

# Generate code from a description
poetry run vaahai generate "Create a Python function that sorts a list of dictionaries by a specified key"

# Apply suggested changes
poetry run vaahai apply --file review_suggestions.json

# Commit changes with AI-generated commit message
poetry run vaahai commit
```

### Example Workflow

```bash
# Review a Python file
poetry run vaahai review --path ./app.py --focus quality

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
