# Vaahai Documentation

Welcome to the official documentation for Vaahai, an AI-augmented code review CLI tool that combines static analysis with large language models to provide intelligent, context-aware code reviews.

## Table of Contents

1. [Installation](./installation.md)
2. [Getting Started](./getting_started.md)
3. [Usage Guide](./usage.md)
4. [Configuration](./configuration.md)
5. [Commands Reference](./commands.md)
6. [Output Formats](./output_formats.md)
7. [LLM Providers](./llm_providers.md)
8. [Static Analyzers](./static_analyzers.md)
9. [Extending Vaahai](./extending.md)
10. [Troubleshooting](./troubleshooting.md)
11. [FAQ](./faq.md)
12. [Contributing](./contributing.md)

## About Vaahai

Vaahai is a powerful command-line tool that enhances code reviews by combining traditional static analysis with AI-powered contextual understanding. It helps developers identify issues, suggest improvements, and maintain code quality with minimal effort.

### Key Features

- **AI-Augmented Code Reviews**: Combines static analysis with LLM-powered contextual review
- **Multiple Languages**: Supports Python (initially), with plans for PHP, JavaScript, and Vue
- **Interactive Fix Application**: Apply suggested fixes with confirmation
- **Multiple Output Formats**: Terminal, Markdown, and HTML outputs
- **Configurable**: Extensive configuration options via TOML files
- **Extensible**: Plugin architecture for custom analyzers and formatters

### How It Works

Vaahai works by:

1. Scanning your code files
2. Running static analysis tools (pylint, flake8, bandit, etc.)
3. Sending the code and analysis results to an LLM (GPT-4 or local models via Ollama)
4. Processing the LLM's response to generate structured, actionable feedback
5. Presenting the results in your preferred format
6. Optionally helping you apply suggested fixes

## Quick Start

```bash
# Install Vaahai
pip install vaahai

# Set up your OpenAI API key
vaahai config set openai.api_key YOUR_API_KEY

# Review a Python file
vaahai review path/to/your/file.py

# Review with interactive fix application
vaahai review path/to/your/file.py --apply-fixes

# See all available commands
vaahai --help
```

## Getting Help

If you need help with Vaahai, you can:

- Check the [Troubleshooting](./troubleshooting.md) guide
- Read the [FAQ](./faq.md)
- Open an issue on GitHub

## License

Vaahai is open source software licensed under the MIT license.
