# VaahAI Developer Review Command

The `vaahai dev review` command provides enhanced diagnostics and debugging capabilities for code reviews, designed specifically for VaahAI developers and contributors. This command extends the standard review command with additional features to help diagnose issues, track performance, and debug the review process.

## Usage

```bash
vaahai dev review run [OPTIONS] PATH
```

Where `PATH` can be a file, directory, or URL.

## Options

| Option | Description |
|--------|-------------|
| `--debug-level [off\|info\|debug\|trace]` | Set the debug level for detailed logging (default: off) |
| `--show-config / --no-show-config` | Show detailed configuration information (default: False) |
| `--show-steps / --no-show-steps` | Show detailed step timing information (default: False) |
| `--log-file TEXT` | Path to log file for debug output |
| `--format TEXT` | Output format (rich, markdown, html, interactive) |
| `--apply-changes / --no-apply-changes` | Apply suggested code changes (default: False) |
| `--dry-run / --no-dry-run` | Preview changes without applying them (default: False) |
| `--backup-dir TEXT` | Directory to store backups of modified files |
| `--no-confirm` | Skip confirmation prompts when applying changes |
| `--help` | Show this message and exit |

## Debug Levels

The `--debug-level` option controls the verbosity of logging:

- `off`: No debug information (default)
- `info`: Basic information about the review process
- `debug`: Detailed debugging information
- `trace`: Comprehensive tracing of all operations

## Examples

### Basic Usage

Run a developer review on a file:

```bash
vaahai dev review run path/to/file.py
```

### With Debug Information

Run a review with debug-level logging:

```bash
vaahai dev review run path/to/file.py --debug-level debug
```

### Show Configuration Information

Run a review and display detailed configuration information:

```bash
vaahai dev review run path/to/file.py --show-config
```

### Show Step Timing Information

Run a review and display timing information for each review step:

```bash
vaahai dev review run path/to/file.py --show-steps
```

### Output to HTML Format

Run a review and generate an HTML report:

```bash
vaahai dev review run path/to/file.py --format html
```

### With Trace-Level Logging to File

Run a review with trace-level logging output to a file:

```bash
vaahai dev review run path/to/file.py --debug-level trace --log-file review_debug.log
```

## Environment Variables

The following environment variables can be used to control the behavior of the developer review command:

| Variable | Description |
|----------|-------------|
| `VAAHAI_DEBUG` | Set to `1`, `true`, or `yes` to enable debug mode |
| `VAAHAI_TRACE` | Set to `1`, `true`, or `yes` to enable trace mode |
| `VAAHAI_STEP_TIMING` | Set to `1`, `true`, or `yes` to enable step timing |

## Use Cases

### Debugging Review Steps

When a review step is failing or producing unexpected results, use the debug level to get more information:

```bash
vaahai dev review run path/to/file.py --debug-level debug
```

### Performance Optimization

Identify slow review steps to optimize performance:

```bash
vaahai dev review run path/to/file.py --show-steps
```

### Troubleshooting Configuration Issues

Verify that the configuration is correct:

```bash
vaahai dev review run path/to/file.py --show-config
```

### Detailed Debugging for Contributors

Get comprehensive debugging information when contributing to VaahAI:

```bash
vaahai dev review run path/to/file.py --debug-level trace --log-file debug.log
```

## Differences from Standard Review Command

The developer review command extends the standard `vaahai review` command with:

1. Enhanced debugging capabilities with multiple debug levels
2. Detailed step timing information
3. Configuration validation and display
4. Comprehensive logging options
5. Improved error handling with optional tracebacks

## See Also

- [VaahAI Review Command](review_command.md)
- [VaahAI Configuration](config_command.md)
- [Developer Tools](dev_commands.md)
