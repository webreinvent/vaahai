# Getting Started with Vaahai

This guide will help you get up and running with Vaahai quickly. We'll walk through installation, basic configuration, and your first code review.

## Quick Start

### 1. Installation

Install Vaahai using pip:

```bash
pip install vaahai
```

### 2. Configuration

Set up your OpenAI API key:

```bash
vaahai config set openai.api_key YOUR_API_KEY
```

### 3. Your First Code Review

Review a Python file:

```bash
vaahai review path/to/your/file.py
```

That's it! You've just performed your first AI-augmented code review with Vaahai.

## Step-by-Step Guide

### Installation

1. Ensure you have Python 3.9 or higher installed:
   ```bash
   python --version
   ```

2. Install Vaahai using pip:
   ```bash
   pip install vaahai
   ```

3. Verify the installation:
   ```bash
   vaahai --version
   ```

### Configuration

1. Set up your LLM provider. For OpenAI:
   ```bash
   vaahai config set openai.api_key YOUR_API_KEY
   ```

   For Ollama (requires [Ollama](https://ollama.ai) to be installed):
   ```bash
   vaahai config set llm.provider ollama
   vaahai config set ollama.model codellama
   ```

2. Verify your configuration:
   ```bash
   vaahai config list
   ```

### Basic Usage

#### Reviewing a Single File

1. Review a Python file:
   ```bash
   vaahai review path/to/your/file.py
   ```

2. The review will include:
   - Static analysis results
   - AI-powered contextual feedback
   - Suggested improvements
   - Potential fixes

#### Understanding the Output

The review output is organized into sections:

1. **Summary**: An overview of the code quality and main findings
2. **Issues**: Detailed list of issues found, categorized by severity
3. **Recommendations**: Suggestions for improvement
4. **Fixes**: Specific code changes that could address the issues

#### Applying Fixes

To interactively apply suggested fixes:

```bash
vaahai review path/to/your/file.py --apply-fixes
```

For each suggested fix, you'll see:
1. The issue description
2. The proposed change (as a diff)
3. Options to apply, skip, or modify the fix

## Common Workflows

### Project Setup

Initialize a project with Vaahai configuration:

```bash
cd your-project
vaahai init
```

This creates a `.vaahai` directory with configuration files.

### Regular Code Reviews

Incorporate Vaahai into your development workflow:

1. Write code as usual
2. Before committing, review changes:
   ```bash
   vaahai review path/to/changed/files
   ```
3. Apply suggested fixes:
   ```bash
   vaahai review path/to/changed/files --apply-fixes
   ```
4. Commit your improved code

### Team Integration

For team usage:

1. Share a common configuration:
   ```bash
   vaahai init --template team
   git add .vaahai/config.toml
   git commit -m "Add Vaahai configuration"
   ```

2. Each team member sets their API keys locally:
   ```bash
   vaahai config set --scope global openai.api_key YOUR_API_KEY
   ```

3. Use in code reviews:
   ```bash
   # Review a pull request
   git checkout feature-branch
   vaahai review $(git diff --name-only main | grep '\.py$')
   ```

### CI/CD Integration

Add Vaahai to your CI pipeline:

```yaml
# Example GitHub Actions workflow
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Vaahai
        run: pip install vaahai
      
      - name: Run code review
        env:
          VAAHAI_OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          vaahai review $(git diff --name-only ${{ github.event.pull_request.base.sha }} | grep -E '\.py$') --ci --format markdown --output review.md --exit-code || true
      
      - name: Upload review results
        uses: actions/upload-artifact@v3
        with:
          name: code-review
          path: review.md
```

## Customizing Your Experience

### Changing Output Format

Choose your preferred output format:

```bash
# Terminal output (default)
vaahai review file.py

# Markdown output
vaahai review file.py --format markdown

# HTML output
vaahai review file.py --format html --output review.html
```

### Adjusting Review Depth

Control the thoroughness of reviews:

```bash
# Quick review
vaahai review file.py --depth quick

# Standard review (default)
vaahai review file.py --depth standard

# Deep review
vaahai review file.py --depth deep
```

### Focusing on Specific Areas

Target your reviews to specific concerns:

```bash
# Security focus
vaahai review file.py --focus security

# Performance focus
vaahai review file.py --focus performance

# Style focus
vaahai review file.py --focus style
```

## Next Steps

Now that you're familiar with the basics of Vaahai, you can:

1. Explore the [Usage Guide](./usage.md) for more advanced usage patterns
2. Learn about [Configuration](./configuration.md) options to customize Vaahai
3. Check out the [Commands Reference](./commands.md) for detailed information on all commands
4. Discover how to [Extend Vaahai](./extending.md) with custom analyzers and formatters

## Troubleshooting

### Common Issues

1. **API Key Issues**:
   ```bash
   # Check if API key is set
   vaahai config get openai.api_key
   
   # Reset and set again if needed
   vaahai config set openai.api_key YOUR_API_KEY
   ```

2. **Missing Static Analyzers**:
   ```bash
   # Install required analyzers
   pip install pylint flake8 bandit
   ```

3. **Performance Issues**:
   ```bash
   # Use a lighter review depth
   vaahai review file.py --depth quick
   
   # Or use static analysis only
   vaahai analyze file.py
   ```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting](./troubleshooting.md) guide
2. Read the [FAQ](./faq.md)
3. Open an issue on GitHub with details about your problem
