# Configuration Validation

VaahAI includes a robust configuration validation utility that helps ensure your configuration is complete and valid before running commands.

## Overview

The configuration validation utility checks:

1. Whether the VaahAI configuration exists and has been initialized
2. Whether the selected LLM provider has a valid API key
3. Whether the selected model is valid for the provider
4. Whether the model has the required capabilities for specific commands
5. Whether all required configuration sections are present and valid

## Using the Validation Command

You can validate your configuration using the `vaahai config validate` command:

```bash
# Validate the entire configuration
vaahai config validate

# Validate configuration for a specific command
vaahai config validate --command review

# Attempt to fix configuration issues automatically
vaahai config validate --fix
```

### Command Options

| Option | Description |
|--------|-------------|
| `--command`, `-c` | Validate configuration for a specific command |
| `--fix`, `-f` | Attempt to fix configuration issues automatically |

## Validation Checks

The validation utility performs the following checks:

### Basic Validation

- Checks if the configuration file exists
- Validates the configuration against the schema
- Ensures the selected provider is valid

### Provider-specific Validation

- Checks if the API key is set for the selected provider (except Ollama)
- Validates that the selected model is valid for the provider
- For Ollama, checks if the API base URL is set

### Command-specific Validation

Different VaahAI commands may require specific capabilities:

- `review` and `audit` commands require models with text and code capabilities
- Additional command-specific validations may be added in the future

## Programmatic Usage

You can also use the validation utility programmatically in your Python code:

```python
from vaahai.config.validation import validate_configuration_exists, validate_for_command

# Check if configuration exists
exists, message = validate_configuration_exists()
if not exists:
    print(f"Error: {message}")
    print("Run 'vaahai config init' to set up configuration")
    return

# Validate configuration for a specific command
valid, errors = validate_for_command("review")
if not valid:
    print("Configuration is not valid for 'review' command:")
    for error in errors:
        print(f"- {error}")
    return

# Proceed with command execution
print("Configuration is valid, proceeding with command...")
```

## Automatic Validation

The VaahAI CLI automatically validates configuration before running commands that require it. If validation fails, the command will display an error message and exit.

You can fix most configuration issues by running:

```bash
vaahai config init
```

This will guide you through setting up your configuration with the correct values.

## API Reference

The configuration validation utility provides the following functions:

- `validate_configuration_exists()`: Checks if the configuration file exists
- `validate_configuration_complete()`: Validates the complete configuration
- `validate_for_command(command)`: Validates configuration for a specific command
- `validate_provider_setup(config, provider)`: Validates provider-specific configuration
- `check_model_capabilities(provider, model, required_capabilities)`: Checks if a model has required capabilities
- `get_validation_summary()`: Gets a summary of validation status

See the example script at `examples/config_validation_example.py` for a demonstration of these functions.
