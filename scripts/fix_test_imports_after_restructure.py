#!/usr/bin/env python3
"""
Script to fix test imports after test directory restructuring.
This script updates import paths from 'vaahai.test' to 'tests' in test files.
"""

import os
import re
from pathlib import Path


def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace imports from vaahai.test to tests
    updated_content = re.sub(
        r'from\s+vaahai\.test\.(.*)', 
        r'from tests.\1', 
        content
    )
    
    # Replace imports like 'import vaahai.test.something'
    updated_content = re.sub(
        r'import\s+vaahai\.test\.(.*)', 
        r'import tests.\1', 
        updated_content
    )

    if content != updated_content:
        print(f"Fixing imports in {file_path}")
        with open(file_path, 'w') as file:
            file.write(updated_content)
        return True
    return False


def fix_imports_in_directory(directory):
    """Fix imports in all Python files in the directory and subdirectories."""
    fixed_files = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_imports_in_file(file_path):
                    fixed_files += 1
    return fixed_files


def main():
    """Main function to fix imports in test files."""
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / 'tests'
    
    if not tests_dir.exists():
        print(f"Error: Tests directory {tests_dir} does not exist.")
        return
    
    fixed_files = fix_imports_in_directory(tests_dir)
    print(f"Fixed imports in {fixed_files} files.")


if __name__ == "__main__":
    main()
