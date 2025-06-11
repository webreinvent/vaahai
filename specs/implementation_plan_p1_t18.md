# Implementation Plan for [P1-T18] "Implement LLM provider configuration"

## Overview

This task involves implementing comprehensive configuration support for multiple LLM providers (OpenAI, Claude, Junie, and Ollama) with API keys and provider-specific settings. The implementation will build upon the existing configuration schema and manager.

## Goals

1. Enhance the LLM provider schema with detailed configuration options
2. Implement secure API key management
3. Add provider-specific validation
4. Update the configuration manager to handle provider-specific configurations
5. Create comprehensive tests for LLM provider configuration
6. Document LLM provider configuration options and usage

## Implementation Steps

### Step 1: Enhance LLM Provider Schema

1. Update the existing provider classes in `schema.py` with additional configuration options:
   - Add model validation lists for each provider
   - Add additional provider-specific parameters
   - Implement proper default values
   - Add docstrings for all fields

2. Add secure API key handling:
   - Add methods to securely retrieve API keys
   - Support for keyring/keychain integration (optional)
   - Environment variable fallbacks

### Step 2: Enhance Validation Functions

1. Update the `validate_config` function to include:
   - Model validation for each provider
   - API key validation (presence check)
   - Provider-specific parameter validation
   - Improved error messages

2. Add provider-specific validation functions:
   - `validate_openai_config`
   - `validate_claude_config`
   - `validate_junie_config`
   - `validate_ollama_config`

### Step 3: Update ConfigManager Integration

1. Add methods to ConfigManager for provider-specific operations:
   - `get_current_provider()` - Get the currently configured provider
   - `set_provider(provider)` - Set the active provider
   - `get_provider_config(provider)` - Get configuration for a specific provider
   - `set_api_key(provider, key)` - Set API key for a provider

2. Add convenience methods for common operations:
   - `get_api_key(provider=None)` - Get API key for current or specified provider
   - `get_model(provider=None)` - Get model for current or specified provider
   - `set_model(model, provider=None)` - Set model for current or specified provider

### Step 4: Add LLM Provider Utilities

1. Create a new module `vaahai/config/llm_utils.py` with utility functions:
   - `list_providers()` - List all available providers
   - `list_models(provider)` - List available models for a provider
   - `validate_api_key(provider, key)` - Validate an API key (if possible)
   - `get_default_model(provider)` - Get the default model for a provider

### Step 5: Add Tests

1. Update `test_schema.py` with tests for:
   - Enhanced provider schema validation
   - Model validation
   - API key validation

2. Update `test_manager.py` with tests for:
   - Provider-specific configuration methods
   - API key management

3. Create `test_llm_utils.py` for testing utility functions

### Step 6: Update Documentation

1. Create or update `docs/configuration.md` with:
   - LLM provider configuration options
   - API key management instructions
   - Environment variable overrides
   - Example configurations

2. Add docstrings to all new methods and functions

## Files to Modify

1. `/vaahai/config/schema.py` - Enhance LLM provider schema classes and validation
2. `/vaahai/config/manager.py` - Add provider-specific methods
3. `/vaahai/config/llm_utils.py` (new) - Add LLM provider utilities
4. `/vaahai/test/config/test_schema.py` - Add tests for enhanced schema
5. `/vaahai/test/config/test_manager.py` - Add tests for provider-specific methods
6. `/vaahai/test/config/test_llm_utils.py` (new) - Add tests for utility functions
7. `/docs/configuration.md` (new) - Add documentation for LLM provider configuration

## Acceptance Criteria

1. Users can configure multiple LLM providers with appropriate settings
2. API keys are securely stored and accessed
3. Provider-specific settings are properly validated
4. Configuration can be updated via CLI and environment variables
5. All tests pass with good coverage
6. Documentation is comprehensive and clear

## Dependencies

- [P1-T17] Define configuration schema (Completed)

## Next Steps After Completion

- [P1-T19] Implement model selection
- [P1-T21] Create interactive config command
