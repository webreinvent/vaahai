# Configuration Guide

This guide explains how to configure Vaahai to suit your preferences and requirements. Vaahai uses a TOML-based configuration system with multiple layers of configuration that can be managed through the CLI.

## Configuration Overview

Vaahai's configuration is organized in a hierarchical structure:

1. **Default configuration**: Built-in defaults
2. **Global configuration**: User-level settings in `~/.config/vaahai/config.toml`
3. **Project configuration**: Project-level settings in `.vaahai/config.toml`
4. **Command-line options**: Overrides specified when running commands

Each level overrides the previous levels, giving you flexibility to configure Vaahai globally while allowing per-project customizations.

## Configuration File Structure

Vaahai's configuration file uses TOML format and is organized into sections:

```toml
# General settings
[general]
verbosity = "normal"
output_format = "terminal"

# LLM provider settings
[llm]
provider = "openai"
model = "gpt-4"

# OpenAI specific settings
[openai]
api_key = "your-api-key-here"
temperature = 0.3

# Ollama specific settings
[ollama]
model = "codellama"
host = "http://localhost:11434"

# Static analyzer settings
[analyzers]
enabled = ["pylint", "flake8", "bandit"]

# Pylint specific settings
[analyzers.pylint]
config_file = "~/.pylintrc"

# Review settings
[review]
depth = "standard"
include_related_files = true
apply_fixes_interactively = false

# Output settings
[output]
terminal_colors = true
markdown_format = "github"
html_theme = "light"
```

## Managing Configuration

### Viewing Configuration

To view the current configuration:

```bash
# View all configuration
vaahai config list

# View a specific section
vaahai config list llm

# View a specific setting
vaahai config get llm.provider
```

### Setting Configuration Values

To set configuration values:

```bash
# Set a single value
vaahai config set llm.provider openai

# Set multiple values
vaahai config set openai.api_key YOUR_API_KEY openai.temperature 0.5
```

### Resetting Configuration

To reset configuration to default values:

```bash
# Reset all configuration
vaahai config reset

# Reset a specific section
vaahai config reset llm

# Reset a specific setting
vaahai config reset llm.provider
```

### Configuration Scope

By default, configuration changes are made to the global configuration. To modify project-specific configuration:

```bash
vaahai config set --scope project llm.provider ollama
```

Available scopes:
- `global`: User-level configuration (default)
- `project`: Project-level configuration
- `default`: View default values (read-only)

## Common Configuration Tasks

### Setting Up API Keys

```bash
# Set OpenAI API key
vaahai config set openai.api_key YOUR_API_KEY

# Set other provider keys (if applicable)
vaahai config set anthropic.api_key YOUR_API_KEY
```

### Changing LLM Provider

```bash
# Switch to OpenAI
vaahai config set llm.provider openai
vaahai config set llm.model gpt-4

# Switch to Ollama
vaahai config set llm.provider ollama
vaahai config set llm.model codellama
```

### Configuring Static Analyzers

```bash
# Enable specific analyzers
vaahai config set analyzers.enabled '["pylint", "flake8"]'

# Set analyzer-specific configuration
vaahai config set analyzers.pylint.config_file ~/.custom_pylintrc
vaahai config set analyzers.flake8.ignore 'E501,W503'
```

### Customizing Output

```bash
# Set default output format
vaahai config set general.output_format markdown

# Configure terminal output
vaahai config set output.terminal_colors true
vaahai config set output.terminal_width 100

# Configure markdown output
vaahai config set output.markdown_format github

# Configure HTML output
vaahai config set output.html_theme dark
vaahai config set output.html_include_css true
```

### Setting Review Preferences

```bash
# Set review depth
vaahai config set review.depth deep

# Configure fix application
vaahai config set review.apply_fixes_interactively true
vaahai config set review.auto_apply_safe_fixes false

# Set context inclusion
vaahai config set review.include_related_files true
vaahai config set review.max_related_files 5
```

## Configuration File Locations

Vaahai looks for configuration files in the following locations:

- **Global configuration**: `~/.config/vaahai/config.toml`
- **Project configuration**: `.vaahai/config.toml` (in the current or parent directories)

You can specify a custom configuration file:

```bash
vaahai review file.py --config path/to/config.toml
```

## Environment Variables

You can also configure Vaahai using environment variables. All environment variables should be prefixed with `VAAHAI_`:

```bash
# Set OpenAI API key
export VAAHAI_OPENAI_API_KEY=your-api-key-here

# Set LLM provider
export VAAHAI_LLM_PROVIDER=ollama

# Set output format
export VAAHAI_GENERAL_OUTPUT_FORMAT=markdown
```

Environment variables take precedence over configuration files but are overridden by command-line options.

## Configuration Templates

Vaahai provides configuration templates for common scenarios:

```bash
# Generate a configuration template
vaahai config template > .vaahai/config.toml

# Generate a specific template
vaahai config template --scenario security-focus > .vaahai/config.toml
```

Available templates:
- `default`: Standard configuration
- `minimal`: Minimal configuration with essential settings
- `security-focus`: Configuration focused on security reviews
- `performance-focus`: Configuration focused on performance reviews
- `team`: Configuration for team usage with shared settings

## Advanced Configuration

### Custom Prompt Templates

You can configure custom prompt templates for different review types:

```toml
[prompts]
code_review = "path/to/code_review.prompt"
security_audit = "path/to/security_audit.prompt"
performance_review = "path/to/performance_review.prompt"
```

### Proxy Configuration

If you're behind a proxy:

```toml
[network]
proxy = "http://proxy.example.com:8080"
ssl_verify = true
timeout = 30
```

### Cache Configuration

Configure caching behavior:

```toml
[cache]
enabled = true
location = "~/.cache/vaahai"
max_size_mb = 100
ttl_hours = 24
```

### Plugin Configuration

If you're using plugins:

```toml
[plugins]
enabled = ["my-custom-plugin"]

[plugins.my-custom-plugin]
option1 = "value1"
option2 = "value2"
```

## Troubleshooting Configuration

If you're experiencing configuration issues:

1. **Check current configuration**:
   ```bash
   vaahai config list --verbose
   ```

2. **Verify configuration file locations**:
   ```bash
   vaahai config locations
   ```

3. **Check for environment variables**:
   ```bash
   env | grep VAAHAI_
   ```

4. **Reset to defaults if needed**:
   ```bash
   vaahai config reset
   ```

5. **Validate configuration**:
   ```bash
   vaahai config validate
   ```

## Next Steps

- Learn about [commands](./commands.md) available in Vaahai
- Explore [output formats](./output_formats.md) for review results
- Understand how to use different [LLM providers](./llm_providers.md)
