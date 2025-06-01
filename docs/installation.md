# Installation Guide

This guide will walk you through the process of installing Vaahai on your system.

## Prerequisites

Before installing Vaahai, ensure you have the following prerequisites:

- **Python**: Version 3.9 or higher
- **pip**: The Python package installer
- **API Key**: An OpenAI API key (for using GPT-4) or Ollama installed (for local models)

## Installation Methods

### Method 1: Using pip (Recommended)

The simplest way to install Vaahai is using pip:

```bash
pip install vaahai
```

For a specific version:

```bash
pip install vaahai==0.1.0
```

To upgrade an existing installation:

```bash
pip install --upgrade vaahai
```

### Method 2: Using Poetry

If you use Poetry for dependency management:

```bash
poetry add vaahai
```

### Method 3: From Source

For the latest development version or to contribute:

```bash
# Clone the repository
git clone https://github.com/webreinvent/vaahai.git
cd vaahai

# Install using Poetry (recommended for development)
poetry install

# Or install using pip
pip install -e .
```

## Verifying Installation

To verify that Vaahai was installed correctly:

```bash
vaahai --version
```

This should display the version number of Vaahai.

## Configuration

After installation, you'll need to configure Vaahai with your API keys and preferences:

### Setting Up OpenAI API Key

```bash
vaahai config set openai.api_key YOUR_API_KEY
```

Replace `YOUR_API_KEY` with your actual OpenAI API key.

### Setting Up Ollama (Optional)

If you want to use local models via Ollama:

1. Install Ollama by following the instructions at [ollama.ai](https://ollama.ai)
2. Pull your preferred model:
   ```bash
   ollama pull codellama
   ```
3. Configure Vaahai to use Ollama:
   ```bash
   vaahai config set llm.provider ollama
   vaahai config set ollama.model codellama
   ```

## Installing Dependencies

Vaahai requires certain static analysis tools to function properly. These are installed automatically as dependencies, but you can also install them manually:

```bash
# For Python code review
pip install pylint flake8 bandit

# For PHP code review (if needed)
# Install PHP_CodeSniffer via Composer
composer global require squizlabs/php_codesniffer

# For JavaScript/Vue code review (if needed)
npm install -g eslint eslint-plugin-vue
```

## System-Specific Instructions

### macOS

No additional steps required beyond the standard installation.

### Linux

No additional steps required beyond the standard installation.

### Windows

Vaahai is primarily designed for Unix-like systems. For Windows users, we recommend using Windows Subsystem for Linux (WSL):

1. Install WSL by following Microsoft's instructions
2. Install a Linux distribution (e.g., Ubuntu)
3. Follow the Linux installation instructions within your WSL environment

## Troubleshooting Installation

If you encounter issues during installation:

### Common Issues

1. **Permission Errors**:
   ```bash
   # Install for current user only
   pip install --user vaahai
   ```

2. **Dependency Conflicts**:
   ```bash
   # Install in a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install vaahai
   ```

3. **Python Version Issues**:
   Ensure you're using Python 3.9 or higher:
   ```bash
   python --version
   ```

4. **Missing Static Analysis Tools**:
   If you see warnings about missing tools:
   ```bash
   pip install pylint flake8 bandit
   ```

### Getting Help

If you continue to experience installation problems:

1. Check the [Troubleshooting](./troubleshooting.md) guide
2. Open an issue on GitHub with details about your system and the error messages

## Next Steps

After installation, check out the [Getting Started](./getting_started.md) guide to learn how to use Vaahai for your first code review.
