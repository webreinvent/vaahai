# Commands Reference

This document provides a comprehensive reference for all commands available in Vaahai, including their options, arguments, and examples.

## Command Structure

Vaahai commands follow this general structure:

```
vaahai [global options] command [command options] [arguments]
```

## Global Options

These options can be used with any command:

| Option | Description | Default |
|--------|-------------|---------|
| `--help`, `-h` | Show help message and exit | |
| `--version`, `-v` | Show version information and exit | |
| `--config FILE` | Specify a custom configuration file | `~/.config/vaahai/config.toml` |
| `--verbose` | Increase output verbosity | `normal` |
| `--quiet` | Decrease output verbosity | |
| `--no-color` | Disable colored output | |
| `--format FORMAT` | Output format (terminal, markdown, html) | `terminal` |
| `--output FILE` | Save output to a file | |

## Main Commands

### `review`

Reviews code files using static analysis and LLM-powered contextual review.

#### Usage

```
vaahai review [options] PATH [PATH...]
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Path to file(s) or directory to review |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--depth {quick,standard,thorough}` | Review depth | `standard` |
| `--focus {all,security,performance,style}` | Focus area for the review | `all` |
| `--output {terminal,markdown,html}` | Output format | `terminal` |
| `--output-file FILE` | Save output to a file | None |
| `--interactive` | Enable interactive fix application | `false` |
| `--include PATTERN` | Patterns to include (can be used multiple times) | None |
| `--exclude PATTERN` | Patterns to exclude (can be used multiple times) | None |
| `--config FILE` | Path to configuration file | None |
| `--save-history` | Save review results to history | `false` |
| `--private` | Use only local resources | `false` |
| `--max-file-size SIZE` | Maximum file size in bytes | 1048576 (1MB) |
| `--agent-config` | Path to agent configuration file for customizing the multi-agent system | None |
| `--execute-code` | Enable code execution during review for dynamic analysis | `false` |
| `--no-execute-code` | Disable code execution during review | `true` |
| `--docker-image IMAGE` | Specify custom Docker image for code execution | Language-specific default |
| `--execution-timeout SECONDS` | Maximum execution time in seconds | 60 |
| `--memory-limit LIMIT` | Memory limit for Docker container (e.g., "512m") | "512m" |
| `--cpu-limit LIMIT` | CPU limit for Docker container (e.g., 1.0) | 1.0 |
| `--network-enabled` | Enable network access in Docker container | `false` |

#### Examples

```bash
# Review a single file
vaahai review main path/to/file.py

# Review a directory recursively
vaahai review main src/

# Review with specific include/exclude patterns
vaahai review main src/ --include="*.py" --exclude="*_test.py"

# Review with specific focus and depth
vaahai review main important_module.py --depth thorough --focus security

# Review with interactive fix application
vaahai review main src/ --interactive

# Review with custom file size limit (500KB)
vaahai review main src/ --max-file-size=512000

# Review with custom agent configuration
vaahai review main src/ --agent-config path/to/agent/config.toml

# Review with code execution enabled
vaahai review main src/ --execute-code

# Review with custom Docker image
vaahai review main src/ --docker-image python:3.9-slim

# Review with custom execution timeout (30 seconds)
vaahai review main src/ --execution-timeout 30

# Review with custom memory limit (1GB)
vaahai review main src/ --memory-limit 1g

# Review with custom CPU limit (2.0)
vaahai review main src/ --cpu-limit 2.0

# Review with network access enabled
vaahai review main src/ --network-enabled
```

#### Code Scanner Integration

The review command uses the Vaahai Code Scanner to identify and filter files for review. The scanner:

1. Automatically excludes common directories like `.git`, `node_modules`, and cache directories
2. Supports glob patterns for including and excluding files
3. Detects programming languages based on file extensions
4. Provides file metadata including size, language, and encoding
5. Can filter files based on content

For more details on the Code Scanner, see the [Code Scanner](scanner.md) documentation.

### `helloworld`

The `helloworld` command runs a simple Hello World agent to validate the Autogen integration framework.

```bash
vaahai helloworld [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--message`, `-m` TEXT | Custom hello world message (default: "Hello, World!") |
| `--api-key` TEXT | OpenAI API key for Autogen integration (overrides global config) |
| `--model` TEXT | Model to use for Autogen (overrides global config) |
| `--temperature` FLOAT | Temperature for model generation (overrides global config) |
| `--save-config`, `-s` | Save provided parameters to global configuration |
| `--help` | Show help message and exit |

### Examples

Run with default message:
```bash
vaahai helloworld
```

Run with custom message:
```bash
vaahai helloworld --message "Hello, Autogen!"
```

Run with API key:
```bash
vaahai helloworld --api-key your_openai_api_key
```

Save API key to global configuration:
```bash
vaahai helloworld --api-key your_openai_api_key --save-config
```

### Implementation

The Hello World command creates and runs a basic `HelloWorldAgent` using Microsoft's Autogen framework. It demonstrates:

1. Creating an Autogen `AssistantAgent` with a custom system message
2. Setting up a `UserProxyAgent` for interaction
3. Initiating a conversation between the agents
4. Processing the response from the assistant agent

This command serves as a simple demonstration of the Autogen integration and provides a foundation for more complex multi-agent interactions in future commands.

### `analyze`

Runs static analysis tools without LLM review.

#### Usage

```
vaahai analyze [options] PATH [PATH...]
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Path to file(s) or directory to analyze |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--analyzers LIST` | Comma-separated list of analyzers to use | All enabled |
| `--ignore LIST` | Comma-separated list of issue codes to ignore | None |
| `--fix` | Apply fixes suggested by static analyzers | `false` |
| `--ci` | Run in CI mode (non-interactive) | `false` |
| `--exit-code` | Return non-zero exit code if issues found | `false` |

#### Examples

```bash
# Analyze a single file
vaahai analyze path/to/file.py

# Analyze with specific analyzers
vaahai analyze file.py --analyzers pylint,flake8

# Analyze and fix issues
vaahai analyze file.py --fix

# Analyze in CI environment
vaahai analyze src/ --ci --format markdown --output analysis.md --exit-code
```

### `config`

Manages Vaahai configuration.

#### Subcommands

##### `config init`

Initializes Vaahai configuration with interactive prompts for common settings.

```bash
vaahai config init [OPTIONS]
```

#### Options

| Option | Description |
|--------|-------------|
| `--force`, `-f` | Overwrite existing configuration file |
| `--non-interactive`, `-n` | Use default values without prompting |
| `--skip-api-key` | Skip API key input in interactive mode |
| `--api-key` TEXT | Set OpenAI API key (will be stored in config file) |
| `--llm-model` TEXT | Set default LLM model |
| `--llm-temperature` FLOAT | Set LLM temperature (0.0-1.0) |
| `--autogen-enabled/--no-autogen-enabled` | Enable or disable Autogen |
| `--autogen-model` TEXT | Set default Autogen model |
| `--autogen-temperature` FLOAT | Set Autogen temperature (0.0-1.0) |
| `--use-docker/--no-use-docker` | Enable or disable Docker for Autogen |

#### Interactive Prompts

When run in interactive mode (default), the command will prompt for:

1. OpenAI API Key (can be skipped with `--skip-api-key` flag)
2. Default LLM model
3. LLM temperature
4. Whether to enable Autogen
5. Autogen default model
6. Autogen temperature
7. Whether to use Docker for Autogen execution

The command will automatically use the `OPENAI_API_KEY` environment variable if available.

#### Examples

```bash
# Interactive configuration with prompts
vaahai config init

# Skip API key prompt in interactive mode
vaahai config init --skip-api-key

# Non-interactive mode with default values
vaahai config init --non-interactive

# Fully automated configuration with custom values
vaahai config init --api-key "your-key" --llm-model "gpt-4-turbo" --llm-temperature 0.5 --autogen-model "gpt-4" --use-docker
```

This will start an interactive configuration process:

```
Initializing configuration file

Interactive Configuration Setup
Please provide values for the following configuration settings:
(Press Enter to accept default values shown in brackets)

LLM Configuration
Note: For security, consider setting the OPENAI_API_KEY environment variable instead.
You can also set it later with: vaahai config set llm.api_key YOUR_API_KEY --global

OpenAI API Key (will be visible): ****************************************
Default LLM Model [gpt-4]: gpt-4-turbo
LLM Temperature (0.0-1.0) [0.7]: 0.6

Autogen Configuration
Enable Autogen [Yes]: 
Autogen Default Model [gpt-3.5-turbo]: gpt-4
Autogen Temperature (0.0-1.0) [0]: 0.1
Use Docker for Autogen [No]: Yes

Configuration file created successfully
Created .vaahai.toml in the current directory

Configuration Summary:
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Setting             ┃ Value       ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ LLM Provider        │ openai      │
│ LLM Model           │ gpt-4-turbo │
│ API Key             │ Set         │
│ LLM Temperature     │ 0.6         │
│ Autogen Enabled     │ Yes         │
│ Autogen Model       │ gpt-4       │
│ Autogen Temperature │ 0.1         │
│ Use Docker          │ Yes         │
└─────────────────────┴─────────────┘

Next Steps:
- Try the Hello World agent: vaahai helloworld
- Edit configuration: vaahai config set <key> <value> --global
```

##### `config list`

Lists configuration values.

```bash
vaahai config list
```

##### `config get`

Gets a specific configuration value.

```bash
vaahai config get llm.provider
```

##### `config set`

Sets configuration values.

```bash
vaahai config set llm.provider openai
```

##### `config reset`

Resets configuration to default values.

```bash
vaahai config reset
```

##### `config template`

Generates a configuration template.

```bash
vaahai config template > .vaahai/config.toml
```

##### `config locations`

Shows configuration file locations.

```bash
vaahai config locations
```

##### `config validate`

Validates the current configuration.

```bash
vaahai config validate
```

### `fix`

Applies fixes to code based on a review or analysis.

#### Usage

```
vaahai fix [options] PATH [PATH...]
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Path to file(s) to fix |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--review FILE` | Review file to use for fixes | None |
| `--interactive` | Apply fixes interactively | `true` |
| `--auto-apply-safe` | Automatically apply safe fixes | `false` |
| `--generate-patches` | Generate patch files instead of applying fixes | `false` |
| `--backup` | Create backup files before applying fixes | `true` |

#### Examples

```bash
# Fix based on a previous review
vaahai fix file.py --review review.md

# Fix interactively
vaahai fix file.py --interactive

# Fix automatically (safe fixes only)
vaahai fix file.py --auto-apply-safe --no-interactive

# Generate patches instead of applying fixes
vaahai fix file.py --generate-patches
```

### `explain`

Explains code using LLM.

#### Usage

```
vaahai explain [options] PATH
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Path to file to explain |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--llm-provider PROVIDER` | LLM provider to use | From config |
| `--model MODEL` | Model to use for explanation | From config |
| `--detail {brief,standard,detailed}` | Level of detail | `standard` |
| `--focus {general,algorithm,architecture,api}` | Focus area for explanation | `general` |
| `--include-related` | Include related files for context | `false` |
| `--context TEXT` | Additional context for explanation | None |

#### Examples

```bash
# Explain a file
vaahai explain path/to/file.py

# Detailed algorithm explanation
vaahai explain algorithm.py --detail detailed --focus algorithm

# Brief API explanation
vaahai explain api.py --detail brief --focus api
```

### `compare`

Compares two versions of code and reviews the differences.

#### Usage

```
vaahai compare [options] OLD_PATH NEW_PATH
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `OLD_PATH` | Path to old version of code |
| `NEW_PATH` | Path to new version of code |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--llm-provider PROVIDER` | LLM provider to use | From config |
| `--model MODEL` | Model to use for comparison | From config |
| `--focus {general,security,performance,style}` | Focus area for comparison | `general` |
| `--context TEXT` | Additional context for comparison | None |

#### Examples

```bash
# Compare two files
vaahai compare old_file.py new_file.py

# Compare with security focus
vaahai compare old_auth.py new_auth.py --focus security

# Compare directories
vaahai compare old_dir/ new_dir/
```

### `init`

Initializes a project for use with Vaahai.

#### Usage

```
vaahai init [options] [PATH]
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `PATH` | Path to initialize (default: current directory) |

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--template {default,minimal,security,performance,team}` | Configuration template to use | `default` |
| `--force` | Overwrite existing configuration | `false` |

#### Examples

```bash
# Initialize current directory
vaahai init

# Initialize with security template
vaahai init --template security

# Initialize a specific directory
vaahai init path/to/project --template team
```

### `version`

Displays version information.

#### Usage

```
vaahai version
```

## Advanced Commands

### `plugin`

Manages Vaahai plugins.

#### Subcommands

##### `plugin list`

Lists installed plugins.

```bash
vaahai plugin list
```

##### `plugin install`

Installs a plugin.

```bash
vaahai plugin install plugin-name
```

##### `plugin uninstall`

Uninstalls a plugin.

```bash
vaahai plugin uninstall plugin-name
```

##### `plugin update`

Updates installed plugins.

```bash
vaahai plugin update
```

### `cache`

Manages the Vaahai cache.

#### Subcommands

##### `cache clear`

Clears the cache.

```bash
vaahai cache clear
```

##### `cache info`

Shows cache information.

```bash
vaahai cache info
```

### `completion`

Generates shell completion scripts.

#### Usage

```
vaahai completion [options] SHELL
```

#### Arguments

| Argument | Description |
|----------|-------------|
| `SHELL` | Shell to generate completion for (bash, zsh, fish) |

#### Examples

```bash
# Generate Bash completion
vaahai completion bash > ~/.bash_completion.d/vaahai

# Generate Zsh completion
vaahai completion zsh > ~/.zsh/completion/_vaahai

# Generate Fish completion
vaahai completion fish > ~/.config/fish/completions/vaahai.fish
```

## Exit Codes

Vaahai uses the following exit codes:

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Input error |
| 4 | API error |
| 5 | Issues found (when using --exit-code) |

## Next Steps

- Learn about [configuration options](./configuration.md)
- Explore [output formats](./output_formats.md)
- Understand [LLM providers](./llm_providers.md)
