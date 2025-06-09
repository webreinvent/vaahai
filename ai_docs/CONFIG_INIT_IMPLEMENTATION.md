# VaahAI Configuration Management System

This document provides comprehensive guidance for implementing and extending the VaahAI configuration management system, including the `vaahai config init` command.

## System Architecture

The configuration management system follows a layered approach:

1. **Default Configuration**: Hardcoded defaults in the codebase
2. **User Configuration**: Global settings in `~/.vaahai/config.toml`
3. **Project Configuration**: Project-specific settings in `./.vaahai/config.toml`
4. **Environment Variables**: Runtime overrides with `VAAHAI_` prefix
5. **Command-line Arguments**: Highest priority overrides

### Key Components

- **ConfigManager**: Central class managing configuration loading, validation, and access
- **Configuration Schema**: Defines structure, types, and validation rules
- **Configuration Loaders**: Handle loading from different sources
- **Configuration Validators**: Ensure configuration integrity
- **Secure Storage**: For sensitive information like API keys

## Configuration File Structure

The configuration is stored in TOML format with the following main sections:

```toml
[llm]
# LLM provider settings
provider = "openai"

[llm.openai]
# OpenAI-specific settings
api_key = ""
model = "gpt-4"

[docker]
# Docker execution settings
enabled = true

[output]
# Output formatting preferences
format = "terminal"

[agents]
# Agent configuration
enabled = ["audit", "review"]

[security]
# Security settings
use_secure_storage = true
```

## Implementation Guidelines

### Configuration Loading

1. Start with default configuration
2. Load and merge user configuration if available
3. Load and merge project configuration if available
4. Apply environment variable overrides
5. Apply command-line argument overrides

### API Key Storage

1. Use system keyring when available
2. Fall back to encrypted file storage if keyring is unavailable
3. Support environment variables for CI/CD environments
4. Never store API keys in plain text

### Configuration Validation

1. Validate configuration schema
2. Validate provider-specific settings
3. Validate model availability
4. Provide helpful error messages for invalid configurations

### Interactive Configuration

1. Use InquirerPy for interactive prompts
2. Provide clear instructions and examples
3. Validate input before saving
4. Support non-interactive mode for automation

## `vaahai config init` Command

The `vaahai config init` command should follow this workflow:

1. Check for existing configuration
2. If force flag is not set and configuration exists, ask for confirmation to overwrite
3. Guide user through configuration process:
   - LLM provider selection
   - API key input
   - Model selection
   - Docker configuration
   - Output preferences
4. Validate all inputs
5. Save configuration to appropriate location
6. Display success message with next steps

### Command Options

- `--non-interactive`: Run in non-interactive mode
- `--skip-api-keys`: Skip API key configuration
- `--skip-docker`: Skip Docker configuration
- `--force`: Overwrite existing configuration
- `--config-file PATH`: Specify configuration file path

## Best Practices

1. **Security First**: Never log or display API keys
2. **Graceful Degradation**: Handle missing or invalid configuration gracefully
3. **Clear Feedback**: Provide clear error messages and warnings
4. **Sensible Defaults**: Choose reasonable defaults for all settings
5. **Comprehensive Documentation**: Document all configuration options
6. **Backward Compatibility**: Maintain compatibility with older configuration formats

## Testing Strategies

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test configuration loading and validation
3. **Mock Tests**: Use mock API responses for provider validation
4. **Environment Tests**: Test with different environment variables
5. **Edge Cases**: Test with invalid or incomplete configurations

## Extension Points

The configuration system is designed to be extensible:

1. **New Providers**: Add new LLM providers by extending the schema
2. **New Models**: Update model lists as providers release new models
3. **New Settings**: Add new configuration sections as needed
4. **Custom Validators**: Add provider-specific validation logic

## Common Pitfalls

1. **Hardcoded Paths**: Always use platform-independent path handling
2. **Missing Validation**: Always validate user input
3. **Insecure Storage**: Never store sensitive information in plain text
4. **Silent Failures**: Always provide clear error messages
5. **Incomplete Documentation**: Document all configuration options

## Future Enhancements

1. **Configuration Migration**: Support migrating from older formats
2. **Configuration Profiles**: Support multiple named profiles
3. **Remote Configuration**: Support loading configuration from remote sources
4. **Configuration UI**: Provide a web UI for configuration
5. **Configuration Export/Import**: Support exporting and importing configurations
