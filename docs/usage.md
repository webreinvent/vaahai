# Usage Guide

This guide explains how to use Vaahai for AI-augmented code reviews. It covers basic and advanced usage patterns, command options, and practical examples.

## Basic Usage

### Reviewing a Single File

To review a single file, use the `review` command followed by the path to the file:

```bash
vaahai review path/to/your/file.py
```

This will:
1. Run static analysis on the file
2. Send the code and analysis results to the configured LLM
3. Display the review results in the terminal

### Reviewing Multiple Files

You can review multiple files by specifying multiple paths:

```bash
vaahai review file1.py file2.py file3.py
```

Or use wildcards to review all files of a certain type:

```bash
vaahai review "*.py"
```

### Reviewing a Directory

To review all supported files in a directory:

```bash
vaahai review path/to/directory
```

By default, this will recursively scan the directory and review all supported files. You can limit the depth of recursion:

```bash
vaahai review path/to/directory --depth 2
```

### Running Only Static Analysis

If you want to run only the static analysis tools without the LLM review:

```bash
vaahai analyze path/to/your/file.py
```

This is faster and doesn't require an API key or internet connection.

## Output Options

### Changing Output Format

Vaahai supports multiple output formats:

```bash
# Terminal output (default)
vaahai review file.py --format terminal

# Markdown output
vaahai review file.py --format markdown

# HTML output
vaahai review file.py --format html
```

### Saving Output to a File

To save the review results to a file:

```bash
vaahai review file.py --output review_results.md
```

The file extension determines the output format, or you can specify it explicitly:

```bash
vaahai review file.py --format html --output review_results.html
```

### Verbosity Levels

Control the amount of information displayed:

```bash
# Minimal output
vaahai review file.py --verbosity minimal

# Normal output (default)
vaahai review file.py --verbosity normal

# Detailed output
vaahai review file.py --verbosity detailed

# Debug output
vaahai review file.py --verbosity debug
```

## Working with Fixes

### Interactive Fix Application

Vaahai can help you apply suggested fixes interactively:

```bash
vaahai review file.py --apply-fixes
```

This will:
1. Present each suggested fix
2. Show a diff of the proposed changes
3. Ask for confirmation before applying
4. Apply the confirmed fixes to the file

### Automatic Fix Application

To automatically apply fixes that are deemed safe:

```bash
vaahai review file.py --apply-fixes --auto-apply-safe
```

This will apply fixes that are unlikely to change the behavior of the code (e.g., formatting fixes, docstring additions).

### Generating Fix Patches

Instead of applying fixes directly, you can generate patch files:

```bash
vaahai review file.py --generate-patches
```

This creates patch files that can be applied later using standard tools:

```bash
git apply fix_001.patch
```

## LLM Options

### Changing LLM Provider

Switch between different LLM providers:

```bash
# Use OpenAI (default)
vaahai review file.py --llm-provider openai

# Use Ollama
vaahai review file.py --llm-provider ollama
```

### Selecting a Model

Choose a specific model for the review:

```bash
# For OpenAI
vaahai review file.py --model gpt-4

# For Ollama
vaahai review file.py --model codellama
```

### Adjusting Review Depth

Control how thorough the review should be:

```bash
# Quick review (faster, less thorough)
vaahai review file.py --depth quick

# Standard review (default)
vaahai review file.py --depth standard

# Deep review (slower, more thorough)
vaahai review file.py --depth deep
```

## Autogen Multi-Agent System

Vaahai uses Microsoft's Autogen framework to implement a sophisticated multi-agent system for code review. This approach allows specialized agents to collaborate on different aspects of code analysis.

### Agent Types

1. **Language Detector Agent**: Identifies programming languages, features, and versions
2. **Framework/CMS Detector Agent**: Identifies frameworks, libraries, and architectural patterns
3. **Standards Analyzer Agent**: Evaluates adherence to coding standards and best practices
4. **Security Auditor Agent**: Identifies security vulnerabilities and recommends improvements
5. **Review Coordinator Agent**: Orchestrates the review process and aggregates findings

### Custom Agent Configuration

You can provide a custom agent configuration file:

```bash
vaahai review path/to/file.py --agent-config path/to/agent_config.toml
```

Example agent configuration file:

```toml
[agents]
max_rounds = 10
termination_message = "REVIEW_COMPLETE"

[agents.language_detector]
name = "LanguageDetector"
model = "gpt-4"
temperature = 0.2
system_message = """You are a Language Detector Agent..."""

# Additional agent configurations...

[group_chat]
max_rounds = 10
speaker_selection_method = "auto"
```

## Autogen Integration

Vaahai integrates Microsoft's Autogen framework to create a sophisticated multi-agent system for code review. This section describes how to use the Autogen integration features.

### Hello World Agent

The Hello World Agent is a simple agent implementation that demonstrates the integration with Microsoft's Autogen framework. It serves as a foundation for more complex agents in the Vaahai project.

### Running the Hello World Agent

You can run the Hello World Agent using the `helloworld` command:

```bash
vaahai helloworld
```

This will create and run a Hello World agent with the default message "Hello, World!".

### Customizing the Message

You can customize the message using the `--message` option:

```bash
vaahai helloworld --message "Hello, Autogen Integration!"
```

### Language Detector Agent

The Language Detector Agent is a specialized agent that analyzes code files to identify programming languages, estimate language versions, detect frameworks, and identify notable language features.

### Running the Language Detector Agent

You can run the Language Detector Agent using the `detect-language` command:

```bash
vaahai detect-language path/to/file.py
```

This will analyze the file and display the detected language, version, frameworks, and features.

### Analyzing Multiple Files or Directories

You can analyze multiple files or entire directories:

```bash
# Analyze multiple files
vaahai detect-language file1.py file2.js file3.rb

# Analyze all files in a directory
vaahai detect-language src/

# Use wildcard patterns
vaahai detect-language *.js
```

### Output Formats

The Language Detector Agent supports multiple output formats:

```bash
# Default table format
vaahai detect-language src/

# JSON output for programmatic use
vaahai detect-language --format json src/

# Markdown output for documentation
vaahai detect-language --format markdown src/
```

### Disabling LLM Analysis

You can disable LLM-based analysis and use only heuristic detection:

```bash
vaahai detect-language --no-llm src/
```

### Using with OpenAI API Key

For full Autogen capabilities, you'll need to provide an OpenAI API key. You can do this in several ways:

1. Set the `OPENAI_API_KEY` environment variable:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   vaahai helloworld
   ```

2. Provide the API key directly in the command:
   ```bash
   vaahai helloworld --api-key your_openai_api_key
   ```

3. Save the API key to the global configuration:
   ```bash
   vaahai helloworld --api-key your_openai_api_key --save-config
   ```
   
   Or using the config command:
   ```bash
   vaahai config set llm.api_key your_openai_api_key --global
   ```

4. Initialize a project configuration file with the API key:
   ```bash
   vaahai config init
   ```
   Then edit the `.vaahai.toml` file to add your API key.

Without an API key, the Hello World agent will run in limited mode and display a warning message with instructions on how to enable full functionality.

### Global Configuration for Autogen

You can configure Autogen settings globally using the `config` command:

```bash
# Set the default model
vaahai config set autogen.default_model gpt-4 --global

# Set the temperature
vaahai config set autogen.temperature 0.7 --global

# Enable/disable Autogen
vaahai config set autogen.enabled true --global
```

These settings will be used by all agents unless overridden by command-line arguments.

### Implementation Details

The Hello World Agent uses Autogen's `AssistantAgent` and `UserProxyAgent` classes to create a simple conversation flow:

1. The `AssistantAgent` is configured with a system message that includes the custom message
2. The `UserProxyAgent` is set up to interact with the assistant agent
3. A conversation is initiated between the agents
4. The response from the assistant agent is processed and returned

This implementation demonstrates the basic usage of Autogen's conversation mechanisms and provides a foundation for more complex multi-agent interactions in future commands.

### Code Structure

The Hello World Agent implementation consists of the following components:

- `VaahaiAgent`: Base agent class with Autogen integration
- `HelloWorldAgent`: Hello World agent implementation using Autogen
- `AgentFactory`: Factory for creating agents
- `helloworld` CLI command: Command for running the Hello World agent

### Next Steps

With the Hello World Agent implementation complete, the next steps include:

1. Implementing the Language Detector Agent
2. Completing the Docker-based Code Executor
3. Enhancing the CLI integration with more configuration options

### Multi-Agent Code Review

Vaahai uses Microsoft's Autogen framework to implement a sophisticated multi-agent system for code review. This approach allows specialized agents to collaborate on different aspects of code analysis.

#### Using the Multi-Agent System

The multi-agent system is enabled by default for all code reviews. It includes specialized agents for:

- Language detection
- Framework/CMS detection
- Standards analysis
- Security auditing
- Review coordination

To customize the agent system, you can provide a custom configuration file:

```bash
vaahai review path/to/file.py --agent-config path/to/agent_config.toml
```

#### Agent Configuration

A basic agent configuration file looks like this:

```toml
[agents]
# Global agent settings
max_rounds = 10
termination_message = "REVIEW_COMPLETE"

[agents.language_detector]
name = "LanguageDetector"
model = "gpt-4"
temperature = 0.2
system_message = """You are a Language Detector Agent..."""

# Additional agent configurations...
```

For more details, see the [Autogen Integration](autogen_integration.md) documentation.

### Docker-Based Code Execution

Vaahai can execute code during the review process to identify runtime issues and verify suggested fixes.

#### Enabling Code Execution

Code execution is disabled by default for security reasons. To enable it:

```bash
vaahai review path/to/file.py --execute-code
```

#### Customizing Code Execution

You can customize the Docker image used for code execution:

```bash
vaahai review path/to/file.py --execute-code --docker-image="python:3.10-slim"
```

Set a custom execution timeout:

```bash
vaahai review path/to/file.py --execute-code --execution-timeout=30
```

Configure resource limits:

```bash
# Set memory limit to 1GB
vaahai review path/to/file.py --execute-code --memory-limit=1g

# Set CPU limit to 2 cores
vaahai review path/to/file.py --execute-code --cpu-limit=2.0
```

Enable network access (disabled by default for security):

```bash
vaahai review path/to/file.py --execute-code --network-enabled
```

#### Supported Languages

The Docker-based code execution supports multiple programming languages with appropriate Docker images:

| Language | Default Docker Image |
|----------|---------------------|
| Python | python:3.9-slim |
| JavaScript | node:16-alpine |
| Java | openjdk:11-jdk-slim |
| Go | golang:1.17-alpine |
| Rust | rust:1.56-slim |

#### Security Considerations

When using code execution:

- Code is executed in isolated Docker containers
- Network access is disabled by default
- Resource limits are applied to prevent abuse
- Execution timeouts prevent infinite loops
- Containers are automatically cleaned up after execution

## Detecting Programming Languages

To detect programming languages, versions, and frameworks in your code, use the `detect-language` command:

```bash
# Analyze a single file
vaahai detect-language path/to/file.py

# Analyze a directory (recursively)
vaahai detect-language path/to/directory

# Output in different formats
vaahai detect-language path/to/directory --format json
vaahai detect-language path/to/directory --format markdown

# Disable LLM-based analysis
vaahai detect-language path/to/directory --no-llm
```

For more details, see the [Language Detection documentation](language_detection.md).

## Advanced Usage

### Using Project Context

Provide project context for more relevant reviews:

```bash
vaahai review file.py --context "This is a Django web application that handles user authentication and data processing."
```

### Including Related Files

Include related files for context:

```bash
vaahai review file.py --include-related
```

This will automatically identify and include related files (imports, parent classes, etc.) to provide better context for the review.

### Comparing with Previous Version

Review changes compared to a previous version:

```bash
vaahai review file.py --diff
```

This will focus the review on changes since the last commit.

### CI/CD Integration

In CI/CD environments, use non-interactive mode:

```bash
vaahai review file.py --ci --output review.md --exit-code
```

This will:
- Run in non-interactive mode
- Save results to a file
- Return a non-zero exit code if issues are found

### Custom Review Templates

Use a custom prompt template for the review:

```bash
vaahai review file.py --template path/to/template.prompt
```

## Examples

### Basic Code Review

```bash
vaahai review my_script.py
```

### Comprehensive Project Review

```bash
vaahai review src/ --depth deep --format markdown --output review.md
```

### Quick Security Audit

```bash
vaahai review src/ --focus security --analyzers bandit --depth quick
```

### Interactive Fix Session

```bash
vaahai review buggy_code.py --apply-fixes --verbosity detailed
```

### CI Integration

```bash
vaahai review $(git diff --name-only HEAD~1 HEAD | grep '\.py$') --ci --format markdown --output review.md
```

## Next Steps

- Learn how to [configure](./configuration.md) Vaahai to suit your preferences
- Explore the [commands reference](./commands.md) for detailed information on all commands
- Check out [extending Vaahai](./extending.md) to customize it for your needs
