# Configuration Guide

This guide explains how to configure Vaahai to suit your preferences and requirements. Vaahai uses a TOML-based configuration system with multiple layers of configuration that can be managed through the CLI.

## Configuration Overview

Vaahai's configuration is organized in a hierarchical structure with the following precedence (highest to lowest):

1. **Command-line options**: Overrides specified when running commands
2. **Environment variables**: Settings defined with the `VAAHAI_` prefix
3. **User-level config**: Global settings in `~/.config/vaahai/config.toml`
4. **Project-level config**: Project-specific settings in `.vaahai.toml` in the current directory
5. **Default values**: Built-in defaults

Each level overrides the previous levels, giving you flexibility to configure Vaahai globally while allowing per-project customizations and temporary command-line overrides.

## Configuration Architecture

Vaahai uses a modular configuration system built around the singleton pattern to ensure consistent configuration state throughout the application:

1. **Singleton Pattern**: A single `ConfigManager` instance is maintained across the application, accessible via `vaahai.core.config.config_manager`.

2. **Modular Components**:
   - **Data Models**: Type-safe configuration structures using Pydantic models
   - **Validation**: Robust validation for all configuration values
   - **Schema Migration**: Automatic migration of older configuration files
   - **Source Tracking**: Tracking where each configuration value comes from

3. **Extensibility**: The configuration system supports custom keys under the `custom` section that bypass schema validation, allowing for extensibility.

4. **Dynamic Resolution**: Configuration paths are resolved dynamically at runtime to ensure proper handling of environment changes.

## Configuration File Structure

Vaahai's configuration file uses TOML format and is organized into sections:

```toml
# This indicates the schema version of this configuration file
schema_version = 1

# LLM provider settings
[llm]
provider = "openai"
model = "gpt-4"
api_key = "your-api-key-here"
temperature = 0.7
max_tokens = 4000

# Review command settings
[review]
depth = "standard"  # Options: quick, standard, thorough
focus = "all"       # Options: all, security, performance, style
output_format = "terminal"  # Options: terminal, markdown, html
interactive = false
save_history = false
private = false

# Analyze command settings
[analyze]
tools = ["auto"]
output_format = "terminal"
include_metrics = true

# Document command settings
[document]
style = "standard"
output_format = "markdown"
include_examples = true

# Explain command settings
[explain]
depth = "standard"
output_format = "terminal"
include_context = true

# General settings
log_level = "info"

# Custom settings (for extensibility)
[custom]
my_custom_setting = "value"
```

## Schema Versioning and Backward Compatibility

Vaahai configuration files include a `schema_version` field that indicates the version of the configuration schema. This allows Vaahai to automatically migrate older configuration files to the current schema version when they are loaded.

When Vaahai loads a configuration file with an older schema version, it automatically:
- Rename any deprecated fields
- Move fields that have changed location
- Convert values to the appropriate format (e.g., converting "deep" to "thorough" for review depth)

You don't need to manually update your configuration files when upgrading Vaahai. The migration process is automatic and transparent.

## Managing Configuration

### Viewing Configuration

To view the current configuration:

```bash
# View all configuration
vaahai config list

# View a specific section
vaahai config list --section llm

# View a specific setting
vaahai config get llm.provider
```

The `list` command will show all configuration values along with their source (where they were defined).

### Validating Configuration

To validate your configuration against the schema:

```bash
# Validate the entire configuration
vaahai config validate
```

This command checks all configuration values against their expected types and constraints. It will report any validation errors found and exit with a non-zero status code if the configuration is invalid.

Common validation errors include:
- Invalid enum values (e.g., using "deep" instead of "thorough" for review depth)
- Type mismatches (e.g., using a string where a boolean is expected)
- Missing required fields

Example output for a valid configuration:
```
Validating configuration...
Configuration is valid!
```

Example output for an invalid configuration:
```
Validating configuration...
Configuration validation failed with the following errors:
  • review.depth: Value must be one of: 'quick', 'standard', 'thorough'
  • llm.temperature: Value must be a number
```

### Setting Configuration Values

To set configuration values:

```bash
# Set a single value
vaahai config set llm.provider anthropic

# Set multiple values
vaahai config set llm.model claude-3-opus llm.temperature 0.5

# Set nested values
vaahai config set custom.my_setting "custom value"
```

By default, configuration changes are saved to the user-level configuration file. To make session-only changes without saving:

```bash
vaahai config set --no-save llm.provider anthropic
```

### Initializing Project Configuration

To create a project-specific configuration file:

```bash
# Initialize project config in the current directory
vaahai config init

# Force overwrite of existing config
vaahai config init --force
```

This creates a `.vaahai.toml` file in the current directory with basic settings.

## Configuration Options

### LLM Settings

```toml
[llm]
provider = "openai"     # LLM provider (openai, anthropic, etc.)
model = "gpt-4"         # Model to use
api_key = "your-key"    # API key (consider using environment variable instead)
temperature = 0.7       # Temperature for generation (0.0-1.0)
max_tokens = 4000       # Maximum tokens for completion
```

### Review Settings

```toml
[review]
depth = "standard"      # Review depth: quick, standard, thorough
focus = "all"           # Focus area: all, security, performance, style
output_format = "terminal"  # Output format: terminal, markdown, html
interactive = false     # Whether to run in interactive mode
save_history = false    # Whether to save review history
private = false         # Whether to use only local resources
```

### Analyze Settings

```toml
[analyze]
tools = ["auto"]        # Static analysis tools to use, "auto" for automatic selection
output_format = "terminal"  # Output format: terminal, markdown, html
include_metrics = true  # Whether to include metrics in output
```

### Document Settings

```toml
[document]
style = "standard"      # Documentation style: standard, detailed, minimal
output_format = "markdown"  # Output format: markdown, html, rst
include_examples = true # Whether to include examples in documentation
```

### Explain Settings

```toml
[explain]
depth = "standard"      # Explanation depth: quick, standard, thorough
output_format = "terminal"  # Output format: terminal, markdown, html
include_context = true  # Whether to include context in explanations
```

### Custom Settings

You can add any custom settings under the `custom` section:

```toml
[custom]
my_setting = "value"
another_setting = 42
```

Access these with dot notation:

```bash
vaahai config get custom.my_setting
vaahai config set custom.another_setting 100
```

## Environment Variables

You can also configure Vaahai using environment variables. All environment variables should be prefixed with `VAAHAI_` and use uppercase with underscores:

```bash
# Set OpenAI API key
export VAAHAI_LLM_API_KEY=your-api-key-here

# Set LLM provider
export VAAHAI_LLM_PROVIDER=anthropic

# Set review depth
export VAAHAI_REVIEW_DEPTH=thorough
```

Environment variables are converted to configuration keys by:
1. Removing the `VAAHAI_` prefix
2. Converting to lowercase
3. Replacing underscores with dots

For example, `VAAHAI_LLM_PROVIDER` becomes `llm.provider`.

## Configuration File Locations

Vaahai looks for configuration files in the following locations:

- **User-level configuration**: `~/.config/vaahai/config.toml`
- **Project-level configuration**: `.vaahai.toml` in the current directory

## Troubleshooting Configuration

If you're experiencing configuration issues:

1. **Check current configuration with sources**:
   ```bash
   vaahai config list
   ```

2. **Check a specific configuration value**:
   ```bash
   vaahai config get llm.provider
   ```

3. **Validate your configuration**:
   ```bash
   vaahai config validate
   ```

4. **Check for environment variables**:
   ```bash
   env | grep VAAHAI_
   ```

5. **Initialize a new project configuration**:
   ```bash
   vaahai config init --force
   ```

6. **Understand configuration precedence**:
   If a setting isn't taking effect, check its source with `vaahai config list` to see which configuration level is overriding it. Remember the precedence order: CLI args > environment variables > user config > project config > defaults.

7. **Schema version issues**:
   If you encounter errors related to schema version, ensure your configuration files include the `schema_version` field. The system will automatically migrate older schemas, but you can also manually update by adding `schema_version = 1` to your configuration files.

8. **Module import errors**:
   If you're developing with Vaahai and encounter import errors related to the configuration system, use the new package structure:
   ```python
   # Old way (still works but deprecated)
   from vaahai.core.config import config_manager
   
   # New way (recommended)
   from vaahai.core.config import config_manager
   # Or for specific components
   from vaahai.core.config.validation import validate_config
   from vaahai.core.config.models import VaahaiConfig
   ```

## Next Steps

- Learn about [commands](./commands.md) available in Vaahai
- Explore how to use the [review](./commands.md#review) command
- Understand how to use the [analyze](./commands.md#analyze) command
