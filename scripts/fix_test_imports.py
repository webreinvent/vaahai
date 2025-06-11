#!/usr/bin/env python
"""
Script to fix import paths in the merged test files.

This script:
1. Updates import paths from 'vaahai.test' to 'tests'
2. Fixes relative imports
3. Updates conftest.py references

Usage:
    python scripts/fix_test_imports.py
"""

import os
import re
from pathlib import Path


def update_imports_in_file(file_path):
    """Update import statements in the file to reflect the new structure."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Update imports from vaahai.test to tests
    updated_content = re.sub(
        r'from\s+vaahai\.test',
        'from tests',
        content
    )
    updated_content = re.sub(
        r'import\s+vaahai\.test',
        'import tests',
        content
    )

    # Fix relative imports that might be broken
    updated_content = re.sub(
        r'from\s+\.\.\.test',
        'from tests',
        updated_content
    )

    # Write updated content back to file if changes were made
    if content != updated_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        return True
    
    return False


def copy_conftest():
    """Copy conftest.py from vaahai/test to tests directory."""
    src_conftest = Path("/Volumes/Data/Projects/vaahai/vaahai/test/conftest.py")
    dest_conftest = Path("/Volumes/Data/Projects/vaahai/tests/conftest.py")
    
    if src_conftest.exists() and not dest_conftest.exists():
        with open(src_conftest, 'r', encoding='utf-8') as src_file:
            content = src_file.read()
            
        # Update any imports in conftest.py
        content = re.sub(
            r'from\s+vaahai\.test',
            'from tests',
            content
        )
            
        with open(dest_conftest, 'w', encoding='utf-8') as dest_file:
            dest_file.write(content)
        
        print(f"Copied and updated conftest.py")
        return True
    
    return False


def process_directory(directory):
    """Process all Python files in a directory recursively."""
    modified_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if update_imports_in_file(file_path):
                    modified_files.append(file_path)
    
    return modified_files


def main():
    """Main function to fix test imports."""
    tests_dir = Path("/Volumes/Data/Projects/vaahai/tests")
    
    print("Fixing import paths in test files...")
    modified_files = process_directory(tests_dir)
    
    print(f"Updated imports in {len(modified_files)} files")
    
    # Copy conftest.py if needed
    if copy_conftest():
        print("Copied conftest.py to tests directory")
    else:
        print("conftest.py already exists or source not found")
    
    print("\nNext steps:")
    print("1. Run the tests again: poetry run pytest")
    print("2. Fix any remaining test failures manually")
    print("3. Once all tests pass, remove the old test directory: rm -rf vaahai/test")


if __name__ == "__main__":
    main()
