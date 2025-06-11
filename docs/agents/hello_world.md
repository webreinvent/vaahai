# Hello World Agent

The Hello World agent is a simple demonstration agent that showcases the basic functionality of the VaahAI agent system using the new `autogen-agentchat` and `autogen-ext` packages.

## Features

- Generates creative and humorous greeting responses
- Supports project-specific OpenAI API keys (`sk-proj-`)
- Includes test mode for development without API keys
- Uses the prompt management system for customizable prompts
- Demonstrates proper error handling and fallback mechanisms

## Usage

### CLI Usage

You can use the Hello World agent through the VaahAI CLI:

```bash
# Using the direct command
vaahai helloworld

# Using the dev command structure
vaahai dev helloworld

# Run in test mode (no API key required)
vaahai helloworld --test

# Adjust temperature for response generation
vaahai helloworld --temperature 0.9
```

### Programmatic Usage

You can also use the Hello World agent programmatically in your Python code:

```python
from vaahai.agents import AgentFactory

# Create the agent with configuration
config = {
    "name": "HelloWorldAgent",
    "provider": "openai",
    "temperature": 0.7,
    "_test_mode": True  # Set to False to use real API
}

# Create and run the agent
agent = AgentFactory.create_agent("hello_world", config)
result = agent.run()

# Get the response
print(result.get("response"))
```

## Configuration Options

The Hello World agent supports the following configuration options:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | string | `"HelloWorldAgent"` | Custom name for the agent |
| `provider` | string | `"openai"` | LLM provider to use |
| `model` | string | `"gpt-4"` | Model to use for response generation |
| `temperature` | float | `0.7` | Temperature for response generation |
| `_test_mode` | boolean | `false` | Run in test mode without API calls |

## Customizing Prompts

The Hello World agent uses the prompt management system to load and render prompt templates. You can customize the greeting prompt by creating a custom template at:

```
vaahai/agents/applications/hello_world/prompts/greeting.md
```

The template supports the following variables:

- `agent_name`: The name of the agent
- `temperature`: The temperature setting for response generation

## API Key Configuration

The agent will look for API keys in the following locations (in order of precedence):

1. VaahAI configuration (`llm.api_key`)
2. Environment variable `VAAHAI_PROVIDERS_OPENAI_API_KEY`
3. Environment variable `OPENAI_API_KEY`

For project-specific API keys (starting with `sk-proj-`), the agent will automatically set the API type to `"azure"`.

## Example

See the example script at `examples/hello_world_agent_example.py` for a complete demonstration of how to use the Hello World agent.
