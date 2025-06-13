# Interactive Diff Reporter

The `InteractiveDiffReporter` is a powerful component of the VaahAI review system that provides an interactive terminal-based interface for reviewing code issues and applying suggested changes.

## Overview

The Interactive Diff Reporter creates a Rich-based terminal UI that allows users to:
- Navigate between issues and files using keyboard shortcuts
- View side-by-side comparisons of original and suggested code
- Accept or reject suggested code changes
- Apply changes individually or in batch mode
- Undo applied changes
- View a summary of applied and rejected changes

## Key Features

### Interactive Navigation

- **Arrow Keys**: Navigate between issues and files
- **Tab**: Switch between issue list and file view
- **Enter**: View details of the selected issue

### Code Change Management

- **a**: Accept the current suggested code change
- **r**: Reject the current suggested code change
- **b**: Toggle batch mode (collect changes to apply later)
- **p**: Apply all pending changes in batch mode
- **u**: Undo the last applied change
- **q**: Quit and show changes summary

### Visual Indicators

- Severity indicators with emojis (🔴 critical, 🟠 high, 🟡 medium, 🟢 low)
- Status indicators for issues (pending, accepted, rejected)
- Syntax highlighting for code snippets
- Side-by-side diff view with highlighted changes

## Usage

### Basic Usage

The Interactive Diff Reporter is typically used through the VaahAI CLI review command with the `--format interactive` option:

```bash
vaahai review --format interactive path/to/file.py
```

### Enabling Code Change Acceptance

To enable code change acceptance, add the `--apply-changes` flag:

```bash
vaahai review --format interactive --apply-changes path/to/file.py
```

### Additional Options

- `--dry-run`: Preview changes without modifying files
- `--backup-dir`: Specify directory for file backups
- `--no-confirm`: Skip confirmation prompts when applying changes

## Architecture

### Class Structure

```python
class InteractiveDiffReporter:
    def __init__(self, results: Dict[str, Any], console: Optional[Console] = None, 
                code_change_manager: Optional[CodeChangeManager] = None):
        # Initialize with review results, console, and code change manager
        
    def display_interactive_report(self) -> None:
        # Display the interactive report with Rich Live and Layout
        
    def _generate_layout(self) -> Layout:
        # Generate the Rich Layout for the interactive display
        
    def _handle_navigation(self, live: Live) -> None:
        # Handle keyboard navigation and actions
        
    def _accept_current_change(self) -> None:
        # Accept the current suggested code change
        
    def _reject_current_change(self) -> None:
        # Reject the current suggested code change
        
    def _undo_last_change(self) -> None:
        # Undo the last applied change
        
    def _apply_pending_changes(self) -> None:
        # Apply all pending changes in batch mode
        
    def _show_changes_summary(self) -> None:
        # Show a summary of applied and rejected changes
```

### Integration with CodeChangeManager

The Interactive Diff Reporter integrates with the `CodeChangeManager` to:
- Apply code changes to files
- Create backups before modifying files
- Track applied and rejected changes
- Support batch mode and undo functionality

## Example

```python
from rich.console import Console
from vaahai.reporting.interactive_diff_reporter import InteractiveDiffReporter
from vaahai.utils.code_change_manager import CodeChangeManager

# Create a code change manager with configuration
code_change_manager = CodeChangeManager({
    'dry_run': False,
    'confirm_changes': True,
    'backup_dir': '~/.vaahai/backups'
})

# Create an interactive diff reporter with review results
reporter = InteractiveDiffReporter(
    results=review_results,
    console=Console(),
    code_change_manager=code_change_manager
)

# Display the interactive report
reporter.display_interactive_report()
```

## Error Handling

The Interactive Diff Reporter includes robust error handling for:
- Empty or invalid review results
- Files not found or inaccessible
- Failed code changes
- Non-interactive environments

## Related Documentation

- [Review Command](../cli/review_command.md)
- [Code Change Manager](../utils/code_change_manager.md)
- [Review Steps Registry](../review/steps_registry.md)
