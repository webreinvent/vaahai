# Vaahai Usage Guide

This guide provides detailed instructions on how to use Vaahai for various code analysis, review, and improvement tasks.

## Basic Commands

### Getting Help

To see all available commands:

```bash
vaahai --help
```

To get help for a specific command:

```bash
vaahai <command> --help
```

### Configuration

Initialize or update your configuration:

```bash
vaahai config init
```

View your current configuration:

```bash
vaahai config show
```

Set a specific configuration value:

```bash
vaahai config set <key> <value>
```

For example:

```bash
vaahai config set openai.model gpt-4
```

### Hello World

Test your Vaahai installation and LLM connection:

```bash
vaahai helloworld
```

## Code Review

### Basic Review

Review a single file:

```bash
vaahai review path/to/file.py
```

Review an entire directory:

```bash
vaahai review path/to/project/
```

### Review Options

Specify the output format:

```bash
vaahai review path/to/file.py --output markdown
```

Available output formats:
- `terminal` (default): Rich formatted output in the terminal
- `markdown`: Output as a Markdown file
- `html`: Output as an HTML file

Specify the review depth:

```bash
vaahai review path/to/file.py --depth deep
```

Available depth options:
- `quick`: Fast, surface-level review
- `standard` (default): Balanced review
- `deep`: Comprehensive, detailed review

Focus on specific aspects:

```bash
vaahai review path/to/file.py --focus security
```

Available focus options:
- `quality`: Code quality and best practices
- `security`: Security vulnerabilities
- `performance`: Performance issues
- `all` (default): All aspects

Save the review to a file:

```bash
vaahai review path/to/file.py --output markdown --save review.md
```

## Code Audit

### Basic Audit

Perform a comprehensive audit of a project:

```bash
vaahai audit path/to/project/
```

### Audit Options

Specify compliance standards:

```bash
vaahai audit path/to/project/ --standards owasp-top-10,pci-dss
```

Available standards:
- `owasp-top-10`: OWASP Top 10 security risks
- `pci-dss`: Payment Card Industry Data Security Standard
- `hipaa`: Health Insurance Portability and Accountability Act
- `gdpr`: General Data Protection Regulation

Focus on specific aspects:

```bash
vaahai audit path/to/project/ --focus security,compliance
```

Available focus options:
- `security`: Security vulnerabilities
- `compliance`: Regulatory compliance
- `performance`: Performance issues
- `architecture`: Architectural concerns
- `all` (default): All aspects

## Applying Changes

Apply suggested changes from a review:

```bash
vaahai apply path/to/review.md
```

Apply changes interactively:

```bash
vaahai apply path/to/review.md --interactive
```

## Working with Git

Commit applied changes:

```bash
vaahai commit "Fix issues identified in code review"
```

## Advanced Usage

### Using Docker

Enable Docker for code execution:

```bash
vaahai config set docker.enabled true
```

Run a command with Docker explicitly:

```bash
vaahai review path/to/file.py --use-docker
```

### Custom Output Templates

Use a custom template for output:

```bash
vaahai review path/to/file.py --output markdown --template path/to/template.md
```

### Filtering Files

Exclude specific files or directories:

```bash
vaahai review path/to/project/ --exclude "node_modules,*.log"
```

Include only specific file types:

```bash
vaahai review path/to/project/ --include "*.py,*.js"
```

### Batch Processing

Process multiple files or directories:

```bash
vaahai review path1 path2 path3
```

### Using Local LLMs

Configure Vaahai to use Ollama:

```bash
vaahai config set llm.provider ollama
vaahai config set ollama.model llama2
```

## Examples

### Example 1: Quick Security Review

```bash
vaahai review path/to/project/ --focus security --depth quick --output terminal
```

### Example 2: Deep Code Audit with HTML Report

```bash
vaahai audit path/to/project/ --depth deep --output html --save audit-report.html
```

### Example 3: Review and Apply Changes

```bash
# Generate a review
vaahai review path/to/file.py --output markdown --save review.md

# Apply changes interactively
vaahai apply review.md --interactive

# Commit changes
vaahai commit "Fix issues from code review"
```

### Example 4: Custom Review with Specific Standards

```bash
vaahai audit path/to/project/ --standards owasp-top-10 --focus security --output markdown --save security-audit.md
```

## Tips and Best Practices

1. **Start Small**: When first using Vaahai, start with reviewing individual files before moving to entire projects.

2. **Review Suggestions Carefully**: Always review suggested changes before applying them, especially for critical code.

3. **Use Interactive Mode**: For important changes, use the `--interactive` flag to review each change individually.

4. **Combine with Manual Review**: Vaahai is a powerful tool, but it works best when combined with human judgment.

5. **Save Reports**: Use the `--save` option to preserve reports for future reference or sharing with team members.

6. **Configure for Your Project**: Take time to configure Vaahai for your specific project needs using `vaahai config set`.

7. **Use Local LLMs for Sensitive Code**: If working with sensitive code, consider using local LLMs via Ollama to avoid sending code to external APIs.

## Troubleshooting

### Command Fails with API Error

If a command fails with an API error:

1. Check your internet connection
2. Verify your API key is valid
3. Ensure you have sufficient quota with your LLM provider

```bash
# Verify your configuration
vaahai config show

# Test the LLM connection
vaahai helloworld
```

### Review Takes Too Long

If reviews are taking too long:

1. Try using a faster depth setting: `--depth quick`
2. Process smaller chunks of code at a time
3. Consider using a local LLM for faster processing

### Docker Issues

If you encounter Docker-related issues:

1. Ensure Docker is running: `docker ps`
2. Check Docker permissions
3. Try disabling Docker temporarily: `vaahai config set docker.enabled false`
