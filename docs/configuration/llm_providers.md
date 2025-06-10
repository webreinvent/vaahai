# LLM Provider Configuration

VaahAI supports multiple LLM (Large Language Model) providers, allowing you to choose the best provider for your needs. This document describes how to configure and use different LLM providers in VaahAI.

## Supported Providers

VaahAI currently supports the following LLM providers:

- **OpenAI** - GPT models including GPT-4, GPT-4-turbo, and GPT-3.5-turbo
- **Anthropic Claude** - Claude models including Claude 3 Opus, Sonnet, and Haiku
- **Junie** - Junie models including Junie-8b and Junie-20b
- **Ollama** - Local models including Llama3, Mistral, Mixtral, and more

## Configuration Options

Each provider has its own configuration options:

### OpenAI

```toml
[llm]
provider = "openai"

[llm.openai]
api_key = "your-api-key"
api_base = ""  # Optional, for Azure OpenAI or proxies
organization = ""  # Optional
model = "gpt-4"
temperature = 0.7
max_tokens = 4000
top_p = 1.0
frequency_penalty = 0.0
presence_penalty = 0.0
timeout = 120  # seconds
```

### Claude

```toml
[llm]
provider = "claude"

[llm.claude]
api_key = "your-api-key"
api_base = ""  # Optional, for proxies
model = "claude-3-sonnet-20240229"
temperature = 0.7
max_tokens = 4000
top_p = 1.0
top_k = 40
timeout = 120  # seconds
```

### Junie

```toml
[llm]
provider = "junie"

[llm.junie]
api_key = "your-api-key"
api_base = ""  # Optional
model = "junie-8b"
temperature = 0.7
max_tokens = 4000
top_p = 1.0
timeout = 120  # seconds
```

### Ollama

```toml
[llm]
provider = "ollama"

[llm.ollama]
api_base = "http://localhost:11434"
model = "llama3"
temperature = 0.7
max_tokens = 4000
top_p = 1.0
top_k = 40
repeat_penalty = 1.1
timeout = 120  # seconds
```

## Setting Up LLM Providers

### Using the Configuration File

The easiest way to configure LLM providers is by editing your VaahAI configuration file. This file is located at:

- **User configuration**: `~/.vaahai/config.toml`
- **Project configuration**: `./.vaahai/config.toml` (in your project directory)

You can edit these files directly or use the VaahAI CLI to initialize and update your configuration:

```bash
# Initialize configuration
vaahai config init

# Edit configuration
vaahai config edit
```

### Using Environment Variables

You can override configuration settings using environment variables. Environment variables take precedence over configuration files. Use the `VAAHAI_` prefix followed by the configuration key with underscores instead of dots:

```bash
# Set the active provider
export VAAHAI_LLM_PROVIDER=openai

# Set the API key
export VAAHAI_LLM_OPENAI_API_KEY=your-api-key

# Set the model
export VAAHAI_LLM_OPENAI_MODEL=gpt-4
```

VaahAI also checks for standard environment variables for API keys:

```bash
# Standard environment variables for API keys
export OPENAI_API_KEY=your-api-key
export ANTHROPIC_API_KEY=your-api-key
```

### Using the API

You can also configure LLM providers programmatically using the VaahAI API:

```python
from vaahai.config.manager import ConfigManager

# Create a config manager
config_manager = ConfigManager()

# Set the active provider
config_manager.set_provider("openai")

# Set the API key
config_manager.set_api_key("your-api-key")

# Set the model
config_manager.set_model("gpt-4")

# Save the configuration
config_manager.save()
```

## Available Models

### OpenAI Models

- `gpt-4`
- `gpt-4-turbo`
- `gpt-4-32k`
- `gpt-3.5-turbo`
- `gpt-3.5-turbo-16k`
- `gpt-4o`
- `gpt-4o-mini`

### Claude Models

- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`
- `claude-2.1`
- `claude-2.0`
- `claude-instant-1.2`

### Junie Models

- `junie-8b`
- `junie-20b`
- `junie-large`

### Ollama Models

- `llama3`
- `llama2`
- `mistral`
- `mixtral`
- `phi3`
- `gemma`
- `codellama`
- `qwen`
- `vicuna`
- `orca-mini`

## API Key Management

### Setting API Keys

API keys can be set in several ways:

1. **Configuration file**: Add your API key to the appropriate section in your configuration file.
2. **Environment variables**: Set the appropriate environment variable for your provider.
3. **Programmatically**: Use the `set_api_key` method of the `ConfigManager` class.

### API Key Security

For security reasons:

- API keys are never logged or displayed in full in the console
- Consider using environment variables for API keys instead of storing them in configuration files
- For production use, consider using a secrets management system

## Examples

### Basic Usage

```python
from vaahai.config.manager import ConfigManager

# Create a config manager
config_manager = ConfigManager()

# Get the current provider
provider = config_manager.get_current_provider()
print(f"Current provider: {provider}")

# Get the current model
model = config_manager.get_model()
print(f"Current model: {model}")

# Get the API key
api_key = config_manager.get_api_key()
if api_key:
    print(f"API key is set")
else:
    print(f"API key is not set")
```

### Switching Providers

```python
from vaahai.config.manager import ConfigManager
from vaahai.config.llm_utils import list_models

# Create a config manager
config_manager = ConfigManager()

# Switch to Claude
config_manager.set_provider("claude")

# List available models for Claude
claude_models = list_models("claude")
print(f"Available Claude models: {claude_models}")

# Set a Claude model
config_manager.set_model("claude-3-opus-20240229")

# Save the configuration
config_manager.save()
```

### Using Environment Variables

```python
import os
from vaahai.config.manager import ConfigManager

# Set environment variables
os.environ["VAAHAI_LLM_PROVIDER"] = "openai"
os.environ["VAAHAI_LLM_OPENAI_API_KEY"] = "your-api-key"
os.environ["VAAHAI_LLM_OPENAI_MODEL"] = "gpt-4"

# Create a config manager
config_manager = ConfigManager()

# The environment variables will be used automatically
print(f"Provider: {config_manager.get_current_provider()}")
print(f"Model: {config_manager.get_model()}")
```

## Troubleshooting

### API Key Issues

If you're having issues with API keys:

1. Check that your API key is correct and valid
2. Ensure you've set the API key for the correct provider
3. Check environment variables that might be overriding your configuration
4. Try setting the API key explicitly using `config_manager.set_api_key()`

### Model Selection Issues

If you're having issues with model selection:

1. Check that the model is available for your selected provider
2. Ensure you're using the correct model name (they are case-sensitive)
3. Use `list_models(provider)` to see available models for your provider

### Provider Issues

If you're having issues with providers:

1. Check that you're using a supported provider
2. Ensure the provider is correctly configured
3. Check for any network issues that might prevent connecting to the provider
4. For Ollama, ensure the Ollama server is running locally
