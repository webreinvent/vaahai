# Code Change Manager

The `CodeChangeManager` is a utility class in VaahAI that safely manages the application of suggested code changes to files, with support for backups, validation, batch processing, and undo operations.

## Overview

The Code Change Manager provides a robust framework for applying code changes with safety features:
- Automatic file backups before modifications
- Validation of original code against file content
- Batch processing of multiple changes
- Undo functionality for reverting changes
- Comprehensive tracking of applied and rejected changes

## Key Features

### Safe File Modifications

- Creates timestamped backups before modifying files
- Validates that original code matches file content
- Restores from backup if an error occurs during modification
- Tracks all changes with detailed metadata

### Backup Management

- Configurable backup directory (defaults to `~/.vaahai/backups`)
- Timestamped backup files to prevent overwriting
- Backup history tracking for undo operations
- Cleanup of old backups (configurable)

### Batch Processing

- Collect multiple changes to apply at once
- Group changes by file to minimize file operations
- Apply all pending changes with a single command
- Detailed results of batch operations

### Undo Functionality

- Revert the last applied change
- Restore from backup files
- Track undo history

## Usage

### Basic Usage

```python
from vaahai.utils.code_change_manager import CodeChangeManager

# Create a code change manager
manager = CodeChangeManager()

# Apply a change to a file
success = manager.apply_change(
    file_path="path/to/file.py",
    line_number=10,
    original_code="def old_function():",
    suggested_code="def new_function():"
)

if success:
    print("Change applied successfully")
else:
    print("Failed to apply change")
```

### Batch Mode

```python
# Add changes to batch
manager.add_pending_change(
    file_path="path/to/file1.py",
    line_number=10,
    original_code="old code 1",
    suggested_code="new code 1"
)

manager.add_pending_change(
    file_path="path/to/file2.py",
    line_number=20,
    original_code="old code 2",
    suggested_code="new code 2"
)

# Apply all pending changes
results = manager.apply_pending_changes()
print(f"Applied: {results['applied']}, Failed: {results['failed']}")
```

### Undo Operations

```python
# Undo the last applied change
success = manager.undo_last_change()
if success:
    print("Successfully undid last change")
else:
    print("No changes to undo or undo failed")
```

### Configuration Options

```python
# Create a manager with custom configuration
manager = CodeChangeManager({
    'dry_run': True,              # Preview changes without modifying files
    'confirm_changes': False,     # Skip confirmation prompts
    'backup_dir': './backups',    # Custom backup directory
    'max_backups': 100            # Maximum number of backups to keep
})
```

## Architecture

### Class Structure

```python
class CodeChangeManager:
    def __init__(self, config_path: Optional[str] = None):
        # Initialize with optional configuration file
        
    def apply_change(self, file_path: str, line_number: int, 
                    original_code: str, suggested_code: str) -> bool:
        # Apply a suggested code change to a file
        
    def add_pending_change(self, file_path: str, line_number: int,
                          original_code: str, suggested_code: str) -> None:
        # Add a change to the pending changes list
        
    def apply_pending_changes(self) -> Dict[str, Any]:
        # Apply all pending changes in batch mode
        
    def reject_change(self, file_path: str, line_number: int,
                     original_code: str, suggested_code: str) -> None:
        # Record a rejected change
        
    def undo_last_change(self) -> bool:
        # Undo the last applied change
        
    def backup_file(self, file_path: str) -> str:
        # Create a backup of a file
        
    def get_summary(self) -> Dict[str, Any]:
        # Get a summary of applied and rejected changes
```

### Change Tracking

The Code Change Manager tracks:
- Applied changes with backup paths and timestamps
- Rejected changes with reasons
- Pending changes for batch processing
- Change history for undo operations

## Integration with Review Command

The Code Change Manager is integrated with the VaahAI review command through:
- The `--apply-changes` flag to enable code change acceptance
- The `--dry-run` flag to preview changes without modifying files
- The `--backup-dir` option to specify a custom backup directory
- The `--no-confirm` flag to skip confirmation prompts

## Error Handling

The Code Change Manager includes robust error handling for:
- Files not found or inaccessible
- Permission issues
- Original code not matching file content
- Errors during file modification
- Failed backup creation or restoration

## Related Documentation

- [Review Command](../cli/review_command.md)
- [Interactive Diff Reporter](../reporting/interactive_diff_reporter.md)
