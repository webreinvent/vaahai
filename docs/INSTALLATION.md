# Vaahai Installation Guide

This guide provides step-by-step instructions for installing and configuring Vaahai on your system.

## Prerequisites

Before installing Vaahai, ensure you have the following prerequisites:

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)
- Docker (optional, for containerized code execution)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

The easiest way to install Vaahai is using pip:

```bash
pip install vaahai
```

### Method 2: Install from Source

For the latest development version or to contribute to Vaahai:

```bash
# Clone the repository
git clone https://github.com/webreinvent/vaahai.git

# Navigate to the project directory
cd vaahai

# Install the package in development mode
pip install -e .
```

### Method 3: Using Poetry (Recommended for Developers)

If you prefer using Poetry for dependency management:

```bash
# Clone the repository
git clone https://github.com/webreinvent/vaahai.git

# Navigate to the project directory
cd vaahai

# Install dependencies using Poetry
poetry install
```

## Post-Installation Configuration

After installing Vaahai, you need to configure it with your API keys and preferences:

```bash
# Run the configuration wizard
vaahai config init
```

The configuration wizard will guide you through:

1. Selecting your preferred LLM provider (OpenAI, Claude, Junie, or Ollama)
2. Setting up API keys for the selected provider
3. Configuring default models
4. Setting up Docker integration (optional)

## Manual Configuration

If you prefer to configure Vaahai manually, you can create a `.vaahai.toml` file in your home directory:

```toml
# Example configuration file

[llm]
provider = "openai"  # Options: "openai", "claude", "junie", "ollama"

[openai]
api_key = "your-api-key-here"
model = "gpt-4"

[claude]
api_key = "your-api-key-here"
model = "claude-2"

[junie]
api_key = "your-api-key-here"
model = "junie-8b"

[ollama]
model = "llama2"
api_base = "http://localhost:11434"

[docker]
enabled = true
```

## Environment Variables

You can also configure Vaahai using environment variables:

```bash
# Set LLM provider
export VAAHAI_LLM_PROVIDER=openai

# Set API key
export VAAHAI_OPENAI_API_KEY=your-api-key-here

# Set model
export VAAHAI_OPENAI_MODEL=gpt-4
```

## Verifying Installation

To verify that Vaahai is installed correctly, run:

```bash
vaahai --version
```

You should see the version number of Vaahai printed to the console.

To test the functionality, run:

```bash
vaahai helloworld
```

This command will test the connection to your configured LLM provider and display a greeting message.

## Docker Setup (Optional)

If you want to use Docker for code execution:

1. Install Docker on your system following the [official Docker installation guide](https://docs.docker.com/get-docker/).

2. Enable Docker integration in Vaahai:

```bash
vaahai config set docker.enabled true
```

3. Test Docker integration:

```bash
vaahai test docker
```

## Troubleshooting

### API Key Issues

If you encounter errors related to API keys:

1. Verify that your API key is correct
2. Check that you have sufficient credits/quota with your LLM provider
3. Ensure your API key has the necessary permissions

### Docker Issues

If Docker integration is not working:

1. Verify that Docker is running on your system
2. Ensure your user has permissions to access the Docker daemon
3. Check Docker logs for any errors

### Python Version Issues

If you encounter compatibility issues:

1. Verify that you're using Python 3.8 or higher
2. Consider using a virtual environment to isolate dependencies

## Uninstallation

To uninstall Vaahai:

```bash
pip uninstall vaahai
```

To also remove configuration files:

```bash
rm ~/.vaahai.toml
```
