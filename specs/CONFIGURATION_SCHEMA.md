# VaahAI Configuration Schema

This document defines the schema for the VaahAI configuration file, including all available options, their types, default values, and validation rules.

## Schema Overview

The VaahAI configuration is stored in TOML format and consists of the following main sections:

- `llm`: LLM provider settings
- `docker`: Docker execution settings
- `output`: Output formatting preferences
- `agents`: Agent configuration
- `security`: Security settings

## Schema Definition

### LLM Configuration

```toml
[llm]
# Default LLM provider to use
# Must be one of: "openai", "claude", "junie", "ollama"
provider = "openai"

# OpenAI-specific settings
[llm.openai]
# API key for OpenAI
# Will be stored securely using system keyring when possible
api_key = ""
# API base URL (optional, for OpenAI-compatible APIs)
api_base = ""
# Organization ID (optional)
organization = ""
# Default model to use
# Must be one of: "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"
model = "gpt-4"
# Model parameters
temperature = 0.7
max_tokens = 4000

# Claude-specific settings
[llm.claude]
# API key for Claude
api_key = ""
# Default model to use
# Must be one of: "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
model = "claude-3-sonnet-20240229"
# Model parameters
temperature = 0.7
max_tokens = 4000

# Junie-specific settings
[llm.junie]
# API key for Junie
api_key = ""
# Default model to use
model = "junie-8b"
# Model parameters
temperature = 0.7
max_tokens = 4000

# Ollama-specific settings
[llm.ollama]
# API base URL for Ollama
api_base = "http://localhost:11434"
# Default model to use
model = "llama3"
# Model parameters
temperature = 0.7
max_tokens = 4000
```

### Docker Configuration

```toml
[docker]
# Whether to use Docker for code execution
enabled = true
# Docker image to use
image = "vaahai/execution:latest"
# Resource limits
[docker.resource_limits]
cpu = 2.0
memory = "2g"
```

### Output Configuration

```toml
[output]
# Default output format
# Must be one of: "terminal", "markdown", "html"
format = "terminal"
# Default verbosity level
# Must be one of: "quiet", "normal", "verbose", "debug"
verbosity = "normal"
# Whether to use color in output
color = true
```

### Agent Configuration

```toml
[agents]
# List of enabled agents
enabled = ["audit", "review", "security", "quality"]
# Default timeout for agent operations (in seconds)
timeout = 300
# Whether to cache agent results
cache = true
# Cache expiration time (in hours)
cache_expiration = 24
```

### Security Configuration

```toml
[security]
# Whether to send code to external services
allow_external_code_sharing = false
# Whether to anonymize code before sending
anonymize_code = true
# Whether to use secure storage for API keys
use_secure_storage = true
```

## Validation Rules

1. **Provider Validation**: The `llm.provider` value must be one of the supported providers.
2. **Model Validation**: Each provider's model must be from the list of supported models for that provider.
3. **API Key Validation**: API keys must be present for the selected provider.
4. **Docker Validation**: If Docker is enabled, the image must be specified.
5. **Output Format Validation**: The output format must be one of the supported formats.
6. **Verbosity Validation**: The verbosity level must be one of the supported levels.
7. **Agent Validation**: Enabled agents must be from the list of supported agents.

## Environment Variables

All configuration options can be overridden using environment variables with the `VAAHAI_` prefix. For nested options, use underscores to separate levels.

Examples:
- `VAAHAI_LLM_PROVIDER=openai`
- `VAAHAI_LLM_OPENAI_API_KEY=sk-...`
- `VAAHAI_DOCKER_ENABLED=true`
- `VAAHAI_OUTPUT_FORMAT=markdown`

## Command-Line Overrides

Configuration options can also be overridden using command-line options:

```bash
vaahai --llm-provider=openai --docker-enabled=false command
```

## Configuration Precedence

The precedence order for configuration values is:
1. Command-line options
2. Environment variables
3. Project-specific configuration file
4. User configuration file
5. Default values
