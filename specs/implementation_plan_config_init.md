# Implementation Plan: vaahai config init

## Overview

The `vaahai config init` command is a critical component of the VaahAI CLI that provides an interactive setup wizard for configuring the tool. This document outlines the implementation plan for this command, including its components, dependencies, and testing strategy.

## Components

### 1. Configuration File Structure

- Create a configuration directory structure in the user's home directory (`~/.vaahai/`)
- Define a TOML-based configuration file format (`config.toml`)
- Implement project-level configuration override capability (`./.vaahai/config.toml`)

### 2. Configuration Schema

- Define a comprehensive schema for all configuration options
- Implement validation for each configuration option
- Create default configuration values
- Document the schema in code and user documentation

### 3. LLM Provider Configuration

- Support multiple LLM providers:
  - OpenAI
  - Claude
  - Junie
  - Ollama (local LLMs)
- Implement secure API key storage
- Define provider-specific settings (API base URL, organization ID, etc.)

### 4. Model Selection

- Maintain a list of available models for each provider
- Implement model validation
- Allow setting default models per provider
- Support model parameter configuration (temperature, max tokens, etc.)

### 5. Docker Configuration

- Configure Docker usage for code execution
- Allow selection of Docker image
- Configure resource limits (CPU, memory)
- Implement Docker availability detection

### 6. Interactive Configuration Command

- Create an interactive wizard using InquirerPy
- Implement step-by-step configuration process
- Provide clear instructions and examples
- Support non-interactive mode with environment variables

### 7. Configuration Overrides

- Support environment variable overrides
- Implement command-line option overrides
- Define override precedence rules
- Document override capabilities

### 8. Configuration Utilities

- Create helper functions for accessing configuration
- Implement configuration validation utilities
- Provide warning mechanisms for incomplete configuration
- Create configuration migration utilities for future updates

## Implementation Approach

### Phase 1: Core Configuration Management (Task P1-T16)

1. Create the configuration directory structure
2. Implement basic TOML file loading and saving
3. Define the configuration class structure
4. Implement configuration merging (defaults, user, project, env vars)
5. Create basic tests for configuration loading and saving

### Phase 2: Configuration Schema (Task P1-T17)

1. Define the complete configuration schema
2. Implement schema validation
3. Create default configuration values
4. Document the schema
5. Write tests for schema validation

### Phase 3: Provider Configuration (Tasks P1-T18, P1-T19)

1. Implement LLM provider configuration
2. Create secure API key storage
3. Define model selection and validation
4. Implement provider-specific settings
5. Write tests for provider configuration

### Phase 4: Docker Configuration (Task P1-T20)

1. Implement Docker configuration options
2. Create Docker availability detection
3. Configure resource limits
4. Write tests for Docker configuration

### Phase 5: Interactive Command (Task P1-T21)

1. Create the command structure
2. Implement InquirerPy prompts
3. Build the step-by-step wizard
4. Add non-interactive mode
5. Write tests for the command

### Phase 6: Overrides and Utilities (Tasks P1-T22, P1-T23)

1. Implement environment variable overrides
2. Add command-line option overrides
3. Create configuration utilities
4. Implement warning mechanisms
5. Write tests for overrides and utilities

## Testing Strategy

### Unit Tests

- Test configuration loading and saving
- Test schema validation
- Test configuration merging
- Test API key storage
- Test Docker configuration
- Test override mechanisms

### Integration Tests

- Test the complete configuration process
- Test configuration file creation
- Test configuration overrides
- Test Docker integration
- Test LLM provider validation

### End-to-End Tests

- Test the interactive wizard
- Test non-interactive mode
- Test configuration with real providers (using mock credentials)
- Test Docker configuration with actual Docker

## Dependencies

- Typer: CLI framework
- InquirerPy: Interactive prompts
- Rich: Terminal formatting
- TOML: Configuration file format
- Keyring: Secure API key storage
- Docker SDK: Docker integration

## Documentation

- Update configuration.md with detailed configuration options
- Update commands.md with command usage
- Create examples for common configuration scenarios
- Document environment variables for configuration overrides
- Document configuration file format and schema

## Timeline

- Phase 1 (P1-T16): 1-2 days
- Phase 2 (P1-T17): 1 day
- Phase 3 (P1-T18, P1-T19): 2 days
- Phase 4 (P1-T20): 1 day
- Phase 5 (P1-T21): 2 days
- Phase 6 (P1-T22, P1-T23): 1-2 days

Total estimated time: 8-10 days
