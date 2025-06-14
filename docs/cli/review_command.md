# VaahAI Review Command

The `review` command is a powerful code analysis tool that scans your codebase for issues related to security, performance, style, and other categories. It provides detailed feedback with suggested fixes and supports multiple output formats.

## Command Structure

```bash
vaahai review [OPTIONS] PATH
```

## Arguments

- `PATH`: Path to file or directory to review. Required.

## Options

- `--step-id`, `-s`: Filter review steps by ID (can be used multiple times)
- `--category`, `-c`: Filter review steps by category (security, performance, style, etc.)
- `--severity`, `-v`: Filter review steps by severity (critical, high, medium, low)
- `--tag`, `-t`: Filter review steps by tag (can be used multiple times)
- `--format`, `-f`: Output format (rich, markdown, html, interactive)
- `--apply-changes`, `-a`: Enable code change acceptance in interactive mode
- `--dry-run`, `-d`: Preview changes without modifying files
- `--backup-dir`, `-b`: Directory to store file backups (default: ~/.vaahai/backups)
- `--no-confirm`: Skip confirmation prompts when applying changes
- `--help`: Show this message and exit.

## Output Formats

The review command supports four different output formats:

### Rich (Default)

Terminal output with colorful formatting, emoji indicators, and interactive elements:
- Statistics summary with issue counts by severity and category
- Key findings with visual indicators for severity and category
- Detailed issue list with code snippets and suggested fixes
- Progress tracking with step status indicators

### Markdown

Generates a markdown report file with:
- Summary statistics and key findings
- Detailed issue list with code blocks
- Recommendations for addressing issues
- Saved to a timestamped file and optionally displayed in terminal

### HTML

Creates a fully styled HTML report with:
- Interactive navigation between issues
- Syntax highlighting for code snippets
- Visual indicators for severity levels
- Side-by-side comparison of original and suggested code
- Saved to a timestamped file and optionally opened in browser

### Interactive

Launches an interactive terminal UI that allows you to:
- Navigate between issues with keyboard shortcuts
- View side-by-side comparison of original and suggested code
- Accept or reject suggested code changes
- Apply changes individually or in batch mode
- Undo applied changes

## Code Change Acceptance

When using the interactive output format with the `--apply-changes` flag, you can:

1. Navigate between issues using arrow keys
2. Accept changes with `a` key or reject with `r` key
3. Toggle batch mode with `b` key (collect changes to apply later)
4. Apply pending changes in batch mode with `p` key
5. Undo the last applied change with `u` key
6. Quit and show summary with `q` key

### Safety Features

The code change acceptance mechanism includes several safety features:

- File backups are automatically created before applying changes
- Changes can be previewed in dry-run mode without modifying files
- Confirmation prompts can be enabled/disabled with `--no-confirm` flag
- Original code is validated against file content before applying changes
- Changes can be undone using the backup files

## Examples

### Basic Review

```bash
vaahai review path/to/file.py
```

### Review with Filtering

```bash
vaahai review --category security --severity high path/to/directory
```

### Generate HTML Report

```bash
vaahai review --format html path/to/project
```

### Interactive Review with Code Changes

```bash
vaahai review --format interactive --apply-changes path/to/file.py
```

### Batch Apply Changes with No Confirmation

```bash
vaahai review --format interactive --apply-changes --no-confirm path/to/project
```

### Preview Changes Without Modifying Files

```bash
vaahai review --format interactive --apply-changes --dry-run path/to/file.py
```

## Integration with Review Steps

The review command integrates with the review steps registry to:

1. Discover available review steps based on file type and content
2. Filter steps based on user-provided criteria (ID, category, severity, tags)
3. Execute steps in parallel with progress tracking
4. Collect and aggregate results for reporting

## Related Documentation

- [Review Steps Registry](../review/steps_registry.md)
- [Code Change Manager](../utils/code_change_manager.md)
- [Interactive Diff Reporter](../reporting/interactive_diff_reporter.md)
- [Markdown Reporter](../reporting/markdown_reporter.md)
- [HTML Reporter](../reporting/html_reporter.md)
