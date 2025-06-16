# VaahAI CLI Configuration Initialization

This document explains how to properly initialize and configure the VaahAI CLI using the enhanced configuration wizard.

## Overview

The VaahAI CLI requires proper configuration to connect to LLM providers, set up models, and manage resources. The `vaahai config init` command provides an interactive wizard that guides you through the configuration process with clear instructions and helpful tips.

## Running the Configuration Wizard

To start the configuration process, run:

```bash
vaahai config init
```

This will launch the interactive configuration wizard that guides you through the following steps:

### Step 1: LLM Provider Selection

The wizard will first ask you to select your preferred LLM provider. VaahAI supports multiple providers including:

- **OpenAI**: Widely used and offers strong performance
- **Anthropic Claude**: Provides longer context windows
- **Ollama**: Allows running models locally without API keys

Choose the provider you have an account with or prefer to use.

### Step 2: API Key Configuration

Next, you'll need to provide an API key for authentication with your chosen provider. The wizard provides:

- Provider-specific guidance on how to obtain API keys
- Links to relevant provider websites
- Information about API key formats and security

For Ollama (local models), you may not need an API key if using the default local setup.

### Step 3: Model Selection

After configuring your API key, you'll select a specific model from your chosen provider. The wizard helps you understand:

- Different model capabilities and trade-offs
- Cost considerations for various models
- Which models are optimized for specific tasks

The wizard will also display the capabilities of your selected model to help you confirm it meets your needs.

### Step 4: Docker Configuration

Finally, you can configure Docker settings if you want to run LLMs in containers. The wizard explains:

- Benefits of using Docker for LLM isolation
- How to specify Docker images
- Memory limit configuration to manage resource usage

This step is optional, and you can safely skip it if you're not familiar with Docker.

## Configuration Validation

After completing all steps, the wizard validates your configuration and:

- Confirms if your configuration is complete and valid
- Identifies any issues that need to be addressed
- Provides guidance on how to fix configuration problems
- Suggests next steps to verify your setup

## Command Options

The `vaahai config init` command supports the following options:

- `--dir`, `-d`: Specify a custom configuration directory path
- `--verbose`: Show detailed information during configuration
- `--quiet`: Suppress guidance messages and only show prompts

## Related Commands

After initializing your configuration, you can use these related commands:

- `vaahai config show`: Display your current configuration
- `vaahai config validate`: Validate your configuration and identify issues
- `vaahai config set`: Update specific configuration values
- `vaahai config reset`: Reset configuration to defaults

## Troubleshooting

If you encounter issues during configuration:

1. Check that you have entered the correct API key for your provider
2. Verify your internet connection if connecting to cloud providers
3. Run `vaahai config validate --fix` to identify and fix configuration issues
4. Check the provider's website for any service disruptions

## Best Practices

- Keep your API keys secure and never share them
- Regularly update your configuration as providers release new models
- Use environment variables for API keys in shared or CI/CD environments
- Consider using project-level configuration for project-specific settings
