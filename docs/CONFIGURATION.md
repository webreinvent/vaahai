# Vaahai Configuration Guide

This guide explains how to configure Vaahai to suit your specific needs and preferences.

## Configuration Overview

Vaahai uses a layered configuration system with the following precedence (highest to lowest):

1. Command line arguments
2. Environment variables
3. Project-specific configuration file (`.vaahai/config.toml` in the current directory)
4. User configuration file (`~/.vaahai/config.toml` in the user's home directory)
5. Default values

## Initial Configuration

The easiest way to configure Vaahai is to use the interactive configuration wizard:

```bash
vaahai config init
```

This command will guide you through the configuration process, asking for:

1. **LLM Provider Selection**: Choose between OpenAI, Claude, Junie, or local LLMs via Ollama
2. **API Keys**: Securely store API keys for the selected providers
3. **Model Selection**: Choose default models for each provider
4. **Docker Configuration**: Configure Docker usage for code execution
5. **Output Preferences**: Set default output formats and verbosity

### Non-Interactive Configuration

You can also configure Vaahai non-interactively using environment variables:

```bash
export VAAHAI_OPENAI_API_KEY=sk-...
export VAAHAI_DEFAULT_PROVIDER=openai
export VAAHAI_OPENAI_MODEL=gpt-4
vaahai config init --non-interactive
```

### Configuration Options

The `config init` command supports several options:

| Option | Description | Default |
|--------|-------------|---------|
| `--non-interactive` | Run in non-interactive mode | False |
| `--skip-api-keys` | Skip API key configuration | False |
| `--skip-docker` | Skip Docker configuration | False |
| `--force` | Overwrite existing configuration | False |
| `--config-file PATH` | Specify configuration file path | ~/.vaahai/config.toml |

## Configuration File Format

Vaahai uses TOML (Tom's Obvious, Minimal Language) for configuration files. The configuration file is typically located at:

- `~/.vaahai/config.toml` (user-level configuration)
- `./.vaahai/config.toml` (project-level configuration)

## Configuration Sections

### LLM Provider Configuration

```toml
[llm]
provider = "openai"  # Options: "openai", "claude", "junie", "ollama"
timeout = 60  # Request timeout in seconds
cache = true  # Enable response caching
```

### OpenAI Configuration

```toml
[openai]
api_key = "your-api-key-here"
model = "gpt-4"  # Or "gpt-3.5-turbo", etc.
temperature = 0.7
max_tokens = 4000
```

### Claude Configuration

```toml
[claude]
api_key = "your-api-key-here"
model = "claude-2"  # Or "claude-instant-1", etc.
temperature = 0.7
max_tokens = 4000
```

### Junie Configuration

```toml
[junie]
api_key = "your-api-key-here"
model = "junie-8b"
temperature = 0.7
max_tokens = 4000
```

### Ollama Configuration

```toml
[ollama]
model = "llama2"  # Or "codellama", "mistral", etc.
api_base = "http://localhost:11434"
temperature = 0.7
max_tokens = 4000
```

### Docker Configuration

```toml
[docker]
enabled = true  # Whether to use Docker for code execution
image_prefix = "vaahai"  # Prefix for Docker images
timeout = 30  # Execution timeout in seconds
```

### Output Configuration

```toml
[output]
format = "terminal"  # Default output format: "terminal", "markdown", or "html"
color = true  # Use colored output in terminal
verbose = false  # Include detailed information in output
```

### Review Configuration

```toml
[review]
depth = "standard"  # Default review depth: "quick", "standard", or "deep"
focus = "all"  # Default focus areas: "quality", "security", "performance", or "all"
include_snippets = true  # Include code snippets in reviews
```

### Audit Configuration

```toml
[audit]
depth = "deep"  # Default audit depth: "standard" or "deep"
focus = "all"  # Default focus areas
standards = ["owasp-top-10"]  # Default compliance standards
```

### Agent Configuration

```toml
[agents]
timeout = 60  # Agent execution timeout in seconds

[agents.language_detector]
confidence_threshold = 0.8  # Minimum confidence for language detection

[agents.framework_detector]
confidence_threshold = 0.7  # Minimum confidence for framework detection

[agents.reviewer]
include_code_snippets = true  # Include code snippets in reviews
max_issues = 20  # Maximum number of issues to report

[agents.auditor]
include_references = true  # Include reference links for issues
severity_threshold = "low"  # Minimum severity to report: "critical", "high", "medium", or "low"
```

For detailed information on agent configuration and JSON schema validation requirements, see [AGENT_CONFIGURATION.md](AGENT_CONFIGURATION.md).

## Managing Configuration

### Viewing Configuration

To view your current configuration:

```bash
vaahai config show
```

To view a specific configuration value:

```bash
vaahai config get llm.provider
```

### Setting Configuration Values

To set a specific configuration value:

```bash
vaahai config set openai.api_key "your-api-key-here"
```

To set nested configuration values:

```bash
vaahai config set agents.reviewer.max_issues 30
```

### Resetting Configuration

To reset your configuration to default values:

```bash
vaahai config reset
```

## Environment Variables

All configuration options can be set using environment variables with the `VAAHAI_` prefix and uppercase, underscore-separated keys:

```bash
# Set LLM provider
export VAAHAI_LLM_PROVIDER=openai

# Set API key
export VAAHAI_OPENAI_API_KEY=your-api-key-here

# Set nested configuration
export VAAHAI_AGENTS_REVIEWER_MAX_ISSUES=30
```

## Project-Specific Configuration

You can create a project-specific configuration file that will override the user-level configuration:

```bash
# Create a project configuration file
vaahai config init --project
```

This will create a `.vaahai/config.toml` file in the current directory.

## Configuration Examples

### Minimal Configuration

```toml
[llm]
provider = "openai"

[openai]
api_key = "your-api-key-here"
model = "gpt-4"
```

### Local LLM Configuration

```toml
[llm]
provider = "ollama"

[ollama]
model = "codellama"
api_base = "http://localhost:11434"
```

### Security-Focused Configuration

```toml
[llm]
provider = "ollama"  # Use local LLM for sensitive code

[review]
focus = "security"
depth = "deep"

[audit]
standards = ["owasp-top-10", "pci-dss"]
focus = "security"

[docker]
enabled = false  # Disable Docker for security-sensitive environments
```

### Performance-Optimized Configuration

```toml
[llm]
provider = "openai"
cache = true

[review]
depth = "quick"
include_snippets = false

[agents]
timeout = 30

[agents.reviewer]
max_issues = 10
```

## Advanced Configuration

### Custom Templates

You can specify custom templates for output formatting:

```toml
[output]
template_dir = "/path/to/templates"

[output.templates]
review = "review-template.md"
audit = "audit-template.html"
```

### Proxy Configuration

If you need to use a proxy for API requests:

```toml
[network]
proxy = "http://proxy.example.com:8080"
ssl_verify = true
```

### Logging Configuration

Configure logging behavior:

```toml
[logging]
level = "info"  # Options: "debug", "info", "warning", "error"
file = "~/.vaahai/logs/vaahai.log"
max_size = 10  # Maximum log file size in MB
backup_count = 3  # Number of backup files to keep
```

## Securing API Keys

Vaahai takes security seriously, especially when handling API keys:

1. API keys are stored securely using your system's keyring/keychain when available
2. If a secure keyring is not available, keys are stored in the configuration file with restricted permissions
3. You can use environment variables for API keys to avoid storing them in configuration files

To check if your API keys are stored securely:

```bash
vaahai config security-check
```

## Troubleshooting

### Configuration Not Being Applied

If your configuration changes don't seem to be applied:

1. Check the precedence order (command line args > environment variables > project config > user config)
2. Verify you're modifying the correct configuration file
3. Check for typos in configuration keys

### API Key Issues

If you're having issues with API keys:

1. Verify the key is correct by checking your LLM provider's dashboard
2. Ensure the key has the necessary permissions
3. Try setting the key via an environment variable instead of the configuration file

### Reset to Defaults

If your configuration becomes corrupted:

```bash
vaahai config reset
```

This will reset all settings to their default values.
