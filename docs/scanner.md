# Code Scanner

The Vaahai Code Scanner is a powerful module for identifying, filtering, and processing code files for review. It provides a flexible way to scan directories, apply filters, and extract metadata from files.

## Overview

The Code Scanner is designed to efficiently traverse directories, identify relevant code files, and apply various filters to include or exclude files based on criteria such as:

- File extensions
- File size
- File content
- File paths and patterns
- Programming language

The scanner follows the singleton pattern, ensuring that only one instance exists throughout the application lifecycle.

## Usage

### Basic Usage

```python
from vaahai.core.scanner import code_scanner

# Scan a directory
files = code_scanner.scan_path("/path/to/directory")

# Print information about each file
for file_info in files:
    print(f"Path: {file_info.path}")
    print(f"Size: {file_info.size} bytes")
    print(f"Language: {file_info.language}")
    print(f"Encoding: {file_info.encoding}")
    print("---")
```

### Filtering Files

The scanner provides various methods to filter files:

```python
# Reset scanner to default settings
code_scanner.reset()

# Include only specific file extensions
code_scanner.set_include_extensions(["py", "js", "ts"])

# Exclude specific directories
code_scanner.add_exclude_dirs(["node_modules", "build"])

# Set maximum file size (in bytes)
code_scanner.set_max_file_size(1024 * 1024)  # 1MB

# Include files matching specific patterns
code_scanner.set_include_patterns(["*.py", "src/*.js"])

# Exclude files matching specific patterns
code_scanner.set_exclude_patterns(["*_test.py", "*.min.js"])

# Scan with all these filters applied
files = code_scanner.scan_path("/path/to/directory")
```

### Advanced Filtering

For more advanced filtering, you can use the filter classes directly:

```python
from vaahai.core.scanner import code_scanner
from vaahai.core.scanner.filters import (
    LanguageFilter, 
    SizeFilter, 
    ContentFilter, 
    CompositeFilter
)

# Add a language filter to include only Python and JavaScript files
code_scanner.add_filter(LanguageFilter(["python", "javascript"]))

# Add a size filter to exclude files larger than 1MB
code_scanner.add_filter(SizeFilter(1024 * 1024))

# Add a content filter to find files containing specific text
code_scanner.add_filter(ContentFilter("TODO"))

# Create a composite filter (AND logic)
composite = CompositeFilter([
    LanguageFilter(["python"]),
    ContentFilter("def main")
], require_all=True)

code_scanner.add_filter(composite)

# Scan with these filters
files = code_scanner.scan_path("/path/to/directory")
```

### Loading File Content

To load and analyze file content:

```python
# Scan and automatically load content for all files
files_with_content = code_scanner.scan_and_load_content(["/path/to/directory"])

# Or load content on demand
files = code_scanner.scan_path("/path/to/directory")
for file_info in files:
    content = file_info.load_content()
    # Process content...
```

## CLI Integration

The Code Scanner is integrated with the Vaahai CLI through the `review` command:

```bash
# Review a directory with default settings
vaahai review main /path/to/directory

# Use include/exclude patterns
vaahai review main /path/to/directory --include="*.py" --exclude="*_test.py"

# Set maximum file size
vaahai review main /path/to/directory --max-file-size=1048576
```

## File Information

Each scanned file is represented by a `FileInfo` object with the following attributes:

- `path`: Absolute path to the file
- `relative_path`: Path relative to the scan root
- `size`: File size in bytes
- `language`: Detected programming language (if known)
- `encoding`: Detected file encoding
- `content`: File content (if loaded)

## Default Settings

By default, the Code Scanner:

1. Excludes common directories:
   - Version control: `.git`, `.svn`, `.hg`
   - Dependencies: `node_modules`, `venv`, `.venv`, `env`
   - Build artifacts: `build`, `dist`, `target`, `out`, `bin`, `obj`
   - Cache directories: `__pycache__`, `.pytest_cache`, `.mypy_cache`
   - IDE directories: `.idea`, `.vscode`
   - Hidden directories: `.hidden`

2. Sets a default maximum file size of 1MB

3. Detects programming languages based on file extensions

## Architecture

The Code Scanner follows the singleton pattern and is designed with a modular architecture:

- `scanner.py`: Core scanning functionality and file processing
- `filters.py`: Filter classes for file selection
- `__init__.py`: Package exports and singleton instance

The scanner uses composition to apply multiple filters to files, allowing for flexible and extensible filtering capabilities.
