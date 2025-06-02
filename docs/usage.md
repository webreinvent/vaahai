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

## Advanced Features

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

## Static Analysis Options

### Selecting Specific Analyzers

Choose which static analyzers to use:

```bash
vaahai review file.py --analyzers pylint,flake8
```

### Customizing Analyzer Settings

Use custom configuration files for static analyzers:

```bash
vaahai review file.py --pylint-config path/to/pylintrc
```

### Ignoring Specific Issues

Ignore certain types of issues:

```bash
vaahai review file.py --ignore E501,W503
```

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
