"""
Tests for the configuration manager.

This module tests the configuration loading, saving, and accessing functionality.
"""

import os
import tempfile
from pathlib import Path

import pytest
from pydantic import BaseModel

from vaahai.core.config import (
    ConfigManager, 
    ReviewDepth, 
    ReviewFocus, 
    OutputFormat,
    VaahaiConfig
)


def test_config_defaults():
    """Test that default configuration values are set correctly."""
    config_manager = ConfigManager()
    config_manager.load()
    
    # Check default values
    assert config_manager.get("llm.provider") == "openai"
    assert config_manager.get("llm.model") == "gpt-4"
    assert config_manager.get("review.depth") == ReviewDepth.STANDARD
    assert config_manager.get("review.focus") == ReviewFocus.ALL
    assert config_manager.get("review.output_format") == OutputFormat.TERMINAL


def test_config_cli_args():
    """Test that CLI arguments override defaults."""
    config_manager = ConfigManager()
    
    # Set CLI args
    cli_args = {
        "llm.provider": "anthropic",
        "llm.model": "claude-3-opus",
        "review.depth": ReviewDepth.THOROUGH,
        "review.focus": ReviewFocus.SECURITY,
    }
    
    config_manager.load(cli_args)
    
    # Check that CLI args override defaults
    assert config_manager.get("llm.provider") == "anthropic"
    assert config_manager.get("llm.model") == "claude-3-opus"
    assert config_manager.get("review.depth") == ReviewDepth.THOROUGH
    assert config_manager.get("review.focus") == ReviewFocus.SECURITY
    
    # Check sources
    assert config_manager.get_source("llm.provider") == "cli args"
    assert config_manager.get_source("llm.model") == "cli args"
    assert config_manager.get_source("review.depth") == "cli args"
    assert config_manager.get_source("review.focus") == "cli args"
    
    # Check that other values are still defaults
    assert config_manager.get("review.output_format") == OutputFormat.TERMINAL
    assert config_manager.get_source("review.output_format") == "default"


def test_config_env_vars(monkeypatch):
    """Test that environment variables override defaults but not CLI args."""
    config_manager = ConfigManager()
    
    # Set environment variables
    monkeypatch.setenv("VAAHAI_LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("VAAHAI_LLM_MODEL", "claude-3-opus")
    monkeypatch.setenv("VAAHAI_REVIEW_DEPTH", "thorough")
    
    # Set CLI args (should override env vars)
    cli_args = {
        "llm.model": "gpt-4o",
    }
    
    config_manager.load(cli_args)
    
    # Check that env vars override defaults
    assert config_manager.get("llm.provider") == "anthropic"
    assert config_manager.get_source("llm.provider") == "environment"
    
    # Check that CLI args override env vars
    assert config_manager.get("llm.model") == "gpt-4o"
    assert config_manager.get_source("llm.model") == "cli args"
    
    # Check that env vars override defaults for review.depth
    assert config_manager.get("review.depth") == ReviewDepth.THOROUGH
    assert config_manager.get_source("review.depth") == "environment"


def test_config_file_loading():
    """Test loading configuration from a file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a config file
        config_path = Path(temp_dir) / ".vaahai.toml"
        with open(config_path, "w") as f:
            f.write("""
            [llm]
            provider = "anthropic"
            model = "claude-3-opus"
            
            [review]
            depth = "thorough"
            focus = "security"
            """)
        
        # Create a config manager and point to the temp dir
        config_manager = ConfigManager()
        
        # Monkeypatch the current working directory
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Load config
            config_manager.load()
            
            # Check values
            assert config_manager.get("llm.provider") == "anthropic"
            assert config_manager.get("llm.model") == "claude-3-opus"
            assert config_manager.get("review.depth") == ReviewDepth.THOROUGH
            assert config_manager.get("review.focus") == ReviewFocus.SECURITY
            
            # Check sources
            assert config_manager.get_source("llm.provider") == "project config"
            assert config_manager.get_source("llm.model") == "project config"
            assert config_manager.get_source("review.depth") == "project config"
            assert config_manager.get_source("review.focus") == "project config"
        finally:
            os.chdir(original_cwd)


def test_config_precedence():
    """Test the precedence of configuration sources."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a project config file
        config_path = Path(temp_dir) / ".vaahai.toml"
        with open(config_path, "w") as f:
            f.write("""
            [llm]
            provider = "project_provider"
            model = "project_model"

            [review]
            depth = "thorough"
            focus = "security"
            """)

        # Create a user config dir and file
        user_config_dir = Path(temp_dir) / ".config" / "vaahai"
        user_config_dir.mkdir(parents=True, exist_ok=True)
        user_config_path = user_config_dir / "config.toml"
        with open(user_config_path, "w") as f:
            f.write("""
            [llm]
            provider = "user_provider"
            model = "user_model"

            [review]
            depth = "quick"
            """)

        # Monkeypatch environment
        original_cwd = os.getcwd()
        original_home = os.environ.get("HOME")

        try:
            # Set current working directory and HOME
            os.chdir(temp_dir)
            os.environ["HOME"] = temp_dir

            # Set environment variables
            os.environ["VAAHAI_LLM_PROVIDER"] = "env_provider"

            # Create config manager with CLI args
            config_manager = ConfigManager()
            cli_args = {
                "llm.model": "cli_model",
            }

            # Load config
            config_manager.load(cli_args)

            # Check precedence:
            # CLI args > env vars > user config > project config > defaults

            # CLI args highest precedence
            assert config_manager.get("llm.model") == "cli_model"
            assert config_manager.get_source("llm.model") == "cli args"

            # Env vars override user and project config
            assert config_manager.get("llm.provider") == "env_provider"
            assert config_manager.get_source("llm.provider") == "environment"

            # User config overrides project config
            assert config_manager.get("review.depth") == ReviewDepth.QUICK
            assert config_manager.get_source("review.depth") == "user config"

            # Project config overrides defaults
            assert config_manager.get("review.focus") == ReviewFocus.SECURITY
            assert config_manager.get_source("review.focus") == "project config"
        finally:
            os.chdir(original_cwd)
            if original_home:
                os.environ["HOME"] = original_home
            else:
                del os.environ["HOME"]


def test_set_and_get():
    """Test setting and getting configuration values."""
    config_manager = ConfigManager()
    config_manager.load()
    
    # Set a value
    config_manager.set("llm.provider", "anthropic")
    
    # Check value and source
    assert config_manager.get("llm.provider") == "anthropic"
    assert config_manager.get_source("llm.provider") == "user config"
    
    # Set a nested value that doesn't exist
    config_manager.set("custom.nested.value", 42)
    
    # Check value and source
    assert config_manager.get("custom.nested.value") == 42
    assert config_manager.get_source("custom.nested.value") == "user config"


def test_init_project_config():
    """Test initializing a project configuration file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Change to temp dir
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Create config manager and init project config
            config_manager = ConfigManager()
            result = config_manager.init_project_config()
            
            # Check result
            assert result is True
            
            # Check file exists
            config_path = Path(temp_dir) / ".vaahai.toml"
            assert config_path.exists()
            
            # Try to init again without force
            result = config_manager.init_project_config()
            assert result is False
            
            # Try to init again with force
            result = config_manager.init_project_config(force=True)
            assert result is True
        finally:
            os.chdir(original_cwd)
