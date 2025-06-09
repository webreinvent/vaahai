#!/usr/bin/env python3
"""
Example script to test loading a specific configuration file.
"""

from pathlib import Path
from vaahai.config.manager import ConfigManager
from vaahai.config.schema import VaahAIConfig

# Path to our test configuration file
test_config_path = Path("/Volumes/Data/Projects/vaahai/test_config.toml")

# Create a configuration manager with our test file
config_manager = ConfigManager(config_path=test_config_path)

# Display the loaded configuration
print("Loaded configuration from test_config.toml:")
print(f"LLM Provider: {config_manager.get('llm.provider')}")
print(f"Claude Model: {config_manager.get('llm.claude.model')}")
print(f"Claude API Key: {config_manager.get('llm.claude.api_key')}")
print(f"Docker Enabled: {config_manager.get('docker.enabled')}")
print(f"CPU Limit: {config_manager.get('docker.resource_limits.cpu')}")
print(f"Memory Limit: {config_manager.get('docker.resource_limits.memory')}")
print(f"Output Format: {config_manager.get('output.format')}")
print(f"Verbosity: {config_manager.get('output.verbosity')}")
print(f"Default Agent Timeout: {config_manager.get('agents.default_timeout')}")
print()

# Get the configuration as a schema object
schema = config_manager.get_schema()
print("Configuration as schema object:")
print(f"LLM Provider: {schema.llm.provider}")
print(f"Claude Model: {schema.llm.claude.model}")
print(f"Docker Enabled: {schema.docker.enabled}")
print(f"CPU Limit: {schema.docker.resource_limits.cpu}")
print(f"Output Format: {schema.output.format}")
print()

# Validate the configuration
errors = config_manager.validate()
if errors:
    print(f"Validation errors: {errors}")
else:
    print("Configuration is valid!")
