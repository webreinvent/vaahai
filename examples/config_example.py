#!/usr/bin/env python3
"""
Example script demonstrating the configuration management system.
"""

from pathlib import Path
import os
import tempfile
from vaahai.config.manager import ConfigManager
from vaahai.config.schema import VaahAIConfig, schema_to_config

# Create a configuration manager
config_manager = ConfigManager()

# Display the default configuration
print("Default configuration:")
print(f"LLM Provider: {config_manager.get('llm.provider')}")
print(f"OpenAI Model: {config_manager.get('llm.openai.model')}")
print(f"Docker Enabled: {config_manager.get('docker.enabled')}")
print(f"Output Format: {config_manager.get('output.format')}")
print()

# Modify some configuration values
print("Modifying configuration...")
config_manager.set("llm.provider", "claude")
config_manager.set("llm.claude.model", "claude-3-opus")
config_manager.set("docker.enabled", False)
print()

# Get the configuration as a schema object
schema = config_manager.get_schema()
print("Configuration as schema object:")
print(f"LLM Provider: {schema.llm.provider}")
print(f"Claude Model: {schema.llm.claude.model}")
print(f"Docker Enabled: {schema.docker.enabled}")
print()

# Validate the configuration
errors = config_manager.validate()
print(f"Validation errors: {errors}")
print()

# Set an invalid value and check validation
print("Setting invalid LLM provider...")
config_manager.set("llm.provider", "invalid-provider")
errors = config_manager.validate()
print(f"Validation errors: {errors}")
print()

# Reset to valid configuration
config_manager.set("llm.provider", "openai")
print()

# Test environment variable override
print("Testing environment variable override...")
os.environ["VAAHAI_LLM_PROVIDER"] = "ollama"
os.environ["VAAHAI_LLM_OLLAMA_MODEL"] = "llama3"
print(f"LLM Provider from env: {config_manager.get('llm.provider')}")
print(f"Ollama Model from env: {config_manager.get('llm.ollama.model')}")
print()

# Test CLI override
print("Testing CLI override...")
config_manager.apply_cli_overrides({
    "llm.provider": "junie",
    "output.format": "json"
})
print(f"LLM Provider with CLI override: {config_manager.get('llm.provider')}")
print(f"Output Format with CLI override: {config_manager.get('output.format')}")
print()

# Get full config with all overrides applied
full_config = config_manager.get_full_config()
print("Full configuration with all overrides applied:")
print(f"LLM Provider: {full_config['llm']['provider']}")
print(f"Output Format: {full_config['output']['format']}")
print(f"Ollama Model: {full_config['llm']['ollama']['model']}")
print()

# Save configuration to a temporary location for testing
temp_dir = Path(tempfile.gettempdir()) / "vaahai_test_config"
temp_dir.mkdir(exist_ok=True)
os.environ["VAAHAI_USER_CONFIG_DIR"] = str(temp_dir)

print(f"Saving configuration to {temp_dir}/config.toml")
config_manager.save(user_level=True)
print(f"Configuration saved. Check {temp_dir}/config.toml to see the result.")
