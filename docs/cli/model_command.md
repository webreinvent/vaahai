# Model Command

The `model` command in VaahAI provides functionality for managing and selecting LLM models based on their capabilities, context lengths, and other attributes.

## Overview

VaahAI supports multiple LLM providers (OpenAI, Claude, Junie, Ollama) and their respective models. The `model` command allows you to:

- List available models with filtering options
- Get detailed information about specific models
- Set the current model for a provider
- Get model recommendations based on required capabilities
- View available model capabilities across providers

## Usage

### List Models

List all available models across all providers:

```bash
vaahai model list
```

List models with detailed information:

```bash
vaahai model list --details
```

Filter models by provider:

```bash
vaahai model list --provider openai
```

Filter models by capability:

```bash
vaahai model list --capability vision
```

Filter models by minimum context length:

```bash
vaahai model list --min-context 100000
```

### Get Model Information

Get information about the current model:

```bash
vaahai model info
```

Get information about a specific model:

```bash
vaahai model info gpt-4
```

Specify the provider if the model name is ambiguous:

```bash
vaahai model info llama2 --provider ollama
```

### Set Model

Set the current model for the current provider:

```bash
vaahai model set gpt-4
```

Set the model for a specific provider:

```bash
vaahai model set claude-3-opus --provider claude
```

Set the model without saving the configuration:

```bash
vaahai model set gpt-4 --no-save
```

### Get Model Recommendations

Get a recommended model based on required capabilities:

```bash
vaahai model recommend --capability code
```

Get a recommendation with multiple capabilities:

```bash
vaahai model recommend --capability code --capability vision
```

Set the recommended model as the current model:

```bash
vaahai model recommend --capability code --set
```

Save the configuration after setting the recommended model:

```bash
vaahai model recommend --capability code --set --save
```

### View Model Capabilities

List all available model capabilities:

```bash
vaahai model capabilities
```

Show models with a specific capability:

```bash
vaahai model capabilities --capability vision
```

Filter by provider:

```bash
vaahai model capabilities --capability vision --provider openai
```

## Model Capabilities

VaahAI models can have the following capabilities:

| Capability | Description |
|------------|-------------|
| `text` | Basic text generation and understanding |
| `code` | Code generation and understanding |
| `vision` | Image understanding and processing |
| `audio` | Audio transcription and understanding |
| `embedding` | Vector embedding generation |
| `function_calling` | Structured function calling capabilities |

## Examples

### Finding the Best Model for Code Generation

```bash
# List all models with code capability
vaahai model list --capability code

# Get a recommended model for code generation
vaahai model recommend --capability code

# Set the recommended model as current
vaahai model recommend --capability code --set --save
```

### Working with Vision Models

```bash
# List all models with vision capability
vaahai model list --capability vision

# Get detailed information about vision models
vaahai model list --capability vision --details

# Set a specific vision model
vaahai model set gpt-4-vision
```

### Finding Models with Large Context Windows

```bash
# List models with context length >= 100K tokens
vaahai model list --min-context 100000

# Get detailed information about these models
vaahai model list --min-context 100000 --details
```

## Programmatic Usage

You can also use the model selection functionality programmatically:

```python
from vaahai.config.manager import ConfigManager

# Create a ConfigManager instance
config_manager = ConfigManager()

# Get information about the current model
model_info = config_manager.get_model_info()
print(f"Current model: {model_info['name']}")
print(f"Capabilities: {', '.join(model_info['capabilities'])}")
print(f"Context length: {model_info['context_length']:,} tokens")

# Filter models by capability
code_models = config_manager.filter_models_by_capability("code")
print(f"Models with code capability: {code_models}")

# Get a recommended model for specific capabilities
recommended = config_manager.get_recommended_model(["code", "function_calling"])
print(f"Recommended model: {recommended}")

# Set the recommended model
config_manager.set_model(recommended)
config_manager.save()
```

For a complete example, see the [model_selection_example.py](../../examples/model_selection_example.py) script.
