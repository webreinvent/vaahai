# Implementation Plan: P1-T16 Configuration Management

## Task Overview

**Task ID:** [P1-T16]
**Description:** Implement configuration management
**Dependencies:** [P1-T5] Implement CLI entry point
**Status:** Not Started

This task focuses on creating the core configuration management system for VaahAI, including the configuration file structure and loading/saving mechanisms. This is the foundation for all subsequent configuration-related tasks.

## Implementation Goals

1. Create a configuration directory structure in the user's home directory
2. Implement TOML file loading and saving
3. Define the configuration class structure
4. Implement configuration merging (defaults, user, project, env vars)
5. Create basic tests for configuration loading and saving

## Directory Structure

```
vaahai/
├── config/
│   ├── __init__.py
│   ├── manager.py       # Main configuration manager class
│   ├── schema.py        # Configuration schema definitions
│   ├── defaults.py      # Default configuration values
│   ├── loader.py        # Configuration loading utilities
│   └── utils.py         # Helper functions
├── test/
│   └── config/
│       ├── __init__.py
│       ├── test_manager.py
│       ├── test_loader.py
│       └── test_utils.py
```

## Implementation Details

### 1. Configuration Directory Structure

- Create `~/.vaahai/` directory if it doesn't exist
- Support project-level configuration in `./.vaahai/`
- Handle directory creation with proper permissions
- Implement path resolution for different operating systems

```python
# vaahai/config/utils.py
import os
import platform
from pathlib import Path

def get_user_config_dir() -> Path:
    """Get the user's configuration directory."""
    home = Path.home()
    return home / ".vaahai"

def get_project_config_dir() -> Path:
    """Get the project's configuration directory."""
    return Path(".vaahai")

def ensure_config_dir(path: Path) -> None:
    """Ensure the configuration directory exists."""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        # Set appropriate permissions
        if platform.system() != "Windows":
            os.chmod(path, 0o700)  # Only user can read/write/execute
```

### 2. TOML File Loading and Saving

- Use `tomli` for loading TOML files (Python 3.11+ has built-in support)
- Use `tomli-w` for writing TOML files
- Handle file not found errors gracefully
- Implement atomic file writes for reliability

```python
# vaahai/config/loader.py
import tomli
import tomli_w
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile
import os
import shutil

def load_toml(path: Path) -> Dict[str, Any]:
    """Load a TOML file."""
    if not path.exists():
        return {}

    try:
        with open(path, "rb") as f:
            return tomli.load(f)
    except Exception as e:
        # Log error
        return {}

def save_toml(path: Path, data: Dict[str, Any]) -> bool:
    """Save data to a TOML file atomically."""
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create a temporary file
    fd, temp_path = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            tomli_w.dump(data, f)

        # Atomically replace the target file
        shutil.move(temp_path, path)
        return True
    except Exception as e:
        # Clean up the temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        # Log error
        return False
```

### 3. Configuration Class Structure

- Create a `ConfigManager` class to handle all configuration operations
- Use dataclasses or Pydantic for type-safe configuration
- Implement validation for configuration values
- Support nested configuration sections

```python
# vaahai/config/manager.py
from pathlib import Path
from typing import Dict, Any, Optional
import os
from .loader import load_toml, save_toml
from .utils import get_user_config_dir, get_project_config_dir, ensure_config_dir
from .defaults import DEFAULT_CONFIG

class ConfigManager:
    """Manages VaahAI configuration."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the configuration manager."""
        self.user_config_dir = get_user_config_dir()
        self.project_config_dir = get_project_config_dir()
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from all sources."""
        # Start with defaults
        config = DEFAULT_CONFIG.copy()

        # Load user config
        user_config_path = self.user_config_dir / "config.toml"
        user_config = load_toml(user_config_path)
        self._merge_config(config, user_config)

        # Load project config if it exists
        project_config_path = self.project_config_dir / "config.toml"
        if project_config_path.exists():
            project_config = load_toml(project_config_path)
            self._merge_config(config, project_config)

        # Load from specified path if provided
        if self.config_path and self.config_path.exists():
            custom_config = load_toml(self.config_path)
            self._merge_config(config, custom_config)

        # Apply environment variable overrides
        self._apply_env_overrides(config)

        return config

    def _merge_config(self, base: Dict[str, Any], overlay: Dict[str, Any]) -> None:
        """Merge overlay config into base config."""
        for key, value in overlay.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

    def _apply_env_overrides(self, config: Dict[str, Any]) -> None:
        """Apply environment variable overrides to config."""
        # Implementation will be added in P1-T22
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        keys = key.split(".")
        config = self.config

        # Navigate to the correct nested dictionary
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value

    def save(self, user_level: bool = True) -> bool:
        """Save the configuration."""
        if user_level:
            ensure_config_dir(self.user_config_dir)
            return save_toml(self.user_config_dir / "config.toml", self.config)
        else:
            ensure_config_dir(self.project_config_dir)
            return save_toml(self.project_config_dir / "config.toml", self.config)
```

### 4. Default Configuration

- Define sensible defaults for all configuration options
- Document each default value
- Ensure defaults are compatible with all supported platforms

```python
# vaahai/config/defaults.py
DEFAULT_CONFIG = {
    "llm": {
        "provider": "openai",
        "openai": {
            "api_key": "",
            "api_base": "",
            "organization": "",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 4000
        },
        "claude": {
            "api_key": "",
            "model": "claude-3-sonnet-20240229",
            "temperature": 0.7,
            "max_tokens": 4000
        },
        "junie": {
            "api_key": "",
            "model": "junie-8b",
            "temperature": 0.7,
            "max_tokens": 4000
        },
        "ollama": {
            "api_base": "http://localhost:11434",
            "model": "llama3",
            "temperature": 0.7,
            "max_tokens": 4000
        }
    },
    "docker": {
        "enabled": True,
        "image": "vaahai/execution:latest",
        "resource_limits": {
            "cpu": 2.0,
            "memory": "2g"
        }
    },
    "output": {
        "format": "terminal",
        "verbosity": "normal",
        "color": True
    },
    "agents": {
        "enabled": ["audit", "review", "security", "quality"],
        "timeout": 300,
        "cache": True,
        "cache_expiration": 24
    },
    "security": {
        "allow_external_code_sharing": False,
        "anonymize_code": True,
        "use_secure_storage": True
    }
}
```

## Testing Strategy

### Unit Tests

1. Test configuration directory creation
2. Test TOML loading and saving
3. Test configuration merging
4. Test getting and setting configuration values
5. Test environment variable overrides (placeholder for P1-T22)

```python
# vaahai/test/config/test_manager.py
import pytest
from pathlib import Path
import os
import tempfile
import shutil
from vaahai.config.manager import ConfigManager
from vaahai.config.defaults import DEFAULT_CONFIG

class TestConfigManager:
    def setup_method(self):
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.user_config_dir = self.temp_dir / "user" / ".vaahai"
        self.project_config_dir = self.temp_dir / "project" / ".vaahai"

        # Create directories
        self.user_config_dir.mkdir(parents=True, exist_ok=True)
        self.project_config_dir.mkdir(parents=True, exist_ok=True)

        # Patch the config directory functions
        self.original_get_user_config_dir = vaahai.config.utils.get_user_config_dir
        self.original_get_project_config_dir = vaahai.config.utils.get_project_config_dir

        vaahai.config.utils.get_user_config_dir = lambda: self.user_config_dir
        vaahai.config.utils.get_project_config_dir = lambda: self.project_config_dir

    def teardown_method(self):
        # Restore original functions
        vaahai.config.utils.get_user_config_dir = self.original_get_user_config_dir
        vaahai.config.utils.get_project_config_dir = self.original_get_project_config_dir

        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)

    def test_load_default_config(self):
        """Test loading default configuration."""
        config_manager = ConfigManager()
        assert config_manager.get("llm.provider") == "openai"
        assert config_manager.get("docker.enabled") is True

    def test_get_config_value(self):
        """Test getting configuration values."""
        config_manager = ConfigManager()
        assert config_manager.get("llm.openai.model") == "gpt-4"
        assert config_manager.get("nonexistent.key", "default") == "default"

    def test_set_config_value(self):
        """Test setting configuration values."""
        config_manager = ConfigManager()
        config_manager.set("llm.provider", "claude")
        assert config_manager.get("llm.provider") == "claude"

    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        # Create and save config
        config_manager = ConfigManager()
        config_manager.set("llm.provider", "claude")
        config_manager.save()

        # Create a new manager and check if it loads the saved config
        new_config_manager = ConfigManager()
        assert new_config_manager.get("llm.provider") == "claude"

    def test_merge_config(self):
        """Test merging configurations."""
        # Create user config
        user_config = {"llm": {"provider": "claude"}}
        vaahai.config.loader.save_toml(self.user_config_dir / "config.toml", user_config)

        # Create project config
        project_config = {"docker": {"enabled": False}}
        vaahai.config.loader.save_toml(self.project_config_dir / "config.toml", project_config)

        # Load config and check merging
        config_manager = ConfigManager()
        assert config_manager.get("llm.provider") == "claude"  # From user config
        assert config_manager.get("docker.enabled") is False  # From project config
        assert config_manager.get("llm.openai.model") == "gpt-4"  # From defaults
```

## Integration with CLI

- Register the configuration manager as a dependency in the CLI
- Make it available to all commands
- Add `--config` option to specify custom configuration file

```python
# vaahai/cli/main.py
import typer
from pathlib import Path
from typing import Optional
from vaahai.config.manager import ConfigManager

def get_config_callback(ctx: typer.Context, config_file: Optional[Path] = None) -> ConfigManager:
    """Get the configuration manager."""
    if not hasattr(ctx, "obj") or not ctx.obj:
        ctx.obj = {}

    if "config" not in ctx.obj:
        ctx.obj["config"] = ConfigManager(config_path=config_file)

    return ctx.obj["config"]

def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file",
        callback=get_config_callback,
    ),
    # Other global options...
):
    """VaahAI CLI."""
    pass
```

## Dependencies

- `tomli`: For reading TOML files (Python < 3.11)
- `tomli-w`: For writing TOML files
- `typer`: For CLI integration
- `pathlib`: For path manipulation
- `typing`: For type annotations

## Documentation Updates

- Update `configuration.md` with the new configuration structure
- Document environment variable overrides (placeholder for P1-T22)
- Document configuration file format and schema
- Add examples of common configuration scenarios

## Timeline

- Day 1: Implement configuration directory structure and TOML loading/saving
- Day 2: Implement configuration class structure and default configuration
- Day 3: Write tests and integrate with CLI

## Next Steps

After completing this task, we will proceed to:

1. [P1-T17] Define configuration schema with validation
2. [P1-T18] Implement LLM provider configuration
3. [P1-T19] Implement model selection
4. [P1-T20] Implement Docker configuration
5. [P1-T21] Create interactive config command
6. [P1-T22] Implement configuration overrides
7. [P1-T23] Create configuration utilities
