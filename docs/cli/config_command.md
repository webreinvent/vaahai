# Configuration Management

VaahAI provides a comprehensive configuration management system that allows you to customize various aspects of the tool's behavior. The configuration is stored in TOML files and can be managed using the `vaahai config` command group.

## Configuration Files

VaahAI uses the following configuration files:

- **User configuration**: Located at `~/.vaahai/config.toml`, this file contains user-specific settings.
- **Project configuration**: Located at `./.vaahai/config.toml` in your project directory, this file contains project-specific settings.

Configuration values are loaded with the following precedence (highest to lowest):

1. Command-line options
2. Environment variables (prefixed with `VAAHAI_`)
3. Project configuration
4. User configuration
5. Default values

## Configuration Commands

### Initialize Configuration

```bash
vaahai config init [OPTIONS]
```

Interactively set up your VaahAI configuration, including LLM provider selection, API keys, model preferences, and Docker settings.

**Options:**
- `--dir, -d PATH`: Custom configuration directory path

**Example:**
```bash
vaahai config init
```

This will guide you through a series of prompts to configure:
- Your preferred LLM provider (OpenAI, Claude, Junie, Ollama)
- API key for the selected provider
- Default model for the provider
- Docker settings (if you want to use Docker for running LLMs)

### Show Configuration

```bash
vaahai config show [OPTIONS]
```

Display your current VaahAI configuration settings, including LLM provider, API keys (masked), model preferences, and Docker settings.

**Options:**
- `--file, -f PATH`: Path to specific configuration file to display

**Example:**
```bash
vaahai config show
```

### Get Configuration Value

```bash
vaahai config get KEY
```

Get a specific configuration value using dot notation.

**Arguments:**
- `KEY`: Configuration key in dot notation (e.g., `llm.provider`)

**Example:**
```bash
vaahai config get llm.provider
```

### Set Configuration Value

```bash
vaahai config set [OPTIONS] KEY VALUE
```

Set a specific configuration value using dot notation.

**Arguments:**
- `KEY`: Configuration key in dot notation (e.g., `llm.provider`)
- `VALUE`: Value to set

**Options:**
- `--project, -p`: Set at project level instead of user level

**Examples:**
```bash
# Set the LLM provider to Claude
vaahai config set llm.provider claude

# Set Docker to be enabled
vaahai config set docker.enabled true

# Set a project-level configuration value
vaahai config set llm.provider openai --project
```

### Reset Configuration

```bash
vaahai config reset [OPTIONS]
```

Reset the configuration to default values.

**Options:**
- `--yes, -y`: Skip confirmation prompt

**Example:**
```bash
vaahai config reset
```

## Environment Variables

You can override configuration values using environment variables. The environment variable name is constructed by:
1. Adding the prefix `VAAHAI_`
2. Converting the dot notation to uppercase with underscores

For example:
- `llm.provider` becomes `VAAHAI_LLM_PROVIDER`
- `providers.openai.api_key` becomes `VAAHAI_PROVIDERS_OPENAI_API_KEY`

**Examples:**
```bash
# Set the LLM provider to Claude
export VAAHAI_LLM_PROVIDER=claude

# Set the OpenAI API key
export VAAHAI_PROVIDERS_OPENAI_API_KEY=your-api-key
```

## Configuration Schema

The configuration schema includes the following main sections:

### LLM Settings

```toml
[llm]
provider = "openai"  # Current LLM provider (openai, claude, junie, ollama)
```

### Provider Settings

```toml
[providers.openai]
api_key = "your-api-key"
model = "gpt-4"

[providers.claude]
api_key = "your-api-key"
model = "claude-3-opus-20240229"

[providers.junie]
api_key = "your-api-key"
model = "junie-8b"

[providers.ollama]
model = "llama2"
```

### Docker Settings

```toml
[docker]
enabled = false
image = "custom-image"
memory = "8g"
```

### Output Settings

```toml
[output]
format = "text"  # Output format (text, json, markdown)
color = true     # Whether to use colored output
```

## API Key Security

API keys are sensitive information. VaahAI provides several ways to securely manage your API keys:

1. **Environment Variables**: Set your API keys using environment variables to avoid storing them in configuration files.
   ```bash
   export VAAHAI_PROVIDERS_OPENAI_API_KEY=your-api-key
   ```

2. **Masked Display**: When viewing your configuration with `vaahai config show`, API keys are masked for security.

3. **Project-Level Configuration**: Avoid storing API keys in project-level configuration files that might be committed to version control.

## Related Commands

For model-specific configuration, see the [Model Command](model_command.md) documentation.
