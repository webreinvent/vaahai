#!/usr/bin/env python
"""
Script to merge the two test directories in the VaahAI project.

This script:
1. Copies all tests from /vaahai/test to /tests
2. Updates import paths in test files
3. Moves conftest.py and other test utilities
4. Preserves the directory structure

Usage:
    python scripts/merge_test_directories.py
"""

import os
import re
import shutil
from pathlib import Path


def ensure_directory_exists(directory_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")


def update_imports_in_file(file_path):
    """Update import statements in the file to reflect the new structure."""
    with open(file_path, 'r') as file:
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

    # Write updated content back to file
    with open(file_path, 'w') as file:
        file.write(updated_content)
        
    return content != updated_content


def copy_directory_with_structure(src_dir, dest_dir):
    """Copy directory structure and files, updating imports as needed."""
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)
    
    # Create destination directory if it doesn't exist
    ensure_directory_exists(dest_path)
    
    # Track modified files
    modified_files = []
    
    # Copy files and directories
    for item in src_path.glob('**/*'):
        # Calculate relative path
        relative_path = item.relative_to(src_path)
        target_path = dest_path / relative_path
        
        if item.is_dir():
            # Create directory
            ensure_directory_exists(target_path)
        else:
            # Create parent directories if they don't exist
            ensure_directory_exists(target_path.parent)
            
            # Copy file
            shutil.copy2(item, target_path)
            print(f"Copied: {item} -> {target_path}")
            
            # Update imports if it's a Python file
            if item.suffix == '.py':
                if update_imports_in_file(target_path):
                    modified_files.append(str(target_path))
    
    return modified_files


def create_init_files(directory):
    """Create __init__.py files in all subdirectories."""
    for root, dirs, files in os.walk(directory):
        init_file = os.path.join(root, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Auto-generated during test directory merge\n")
            print(f"Created: {init_file}")


def main():
    """Main function to merge test directories."""
    # Define paths
    project_root = Path(__file__).parent.parent
    vaahai_test_dir = project_root / "vaahai" / "test"
    tests_dir = project_root / "tests"
    
    print(f"Project root: {project_root}")
    print(f"Source test directory: {vaahai_test_dir}")
    print(f"Target test directory: {tests_dir}")
    
    # Copy files with directory structure
    print("\nCopying files and directories...")
    modified_files = copy_directory_with_structure(vaahai_test_dir, tests_dir)
    
    # Create __init__.py files
    print("\nCreating __init__.py files...")
    create_init_files(tests_dir)
    
    # Summary
    print("\nMerge completed!")
    print(f"- Files copied: {sum(1 for _ in Path(vaahai_test_dir).glob('**/*')) - sum(1 for _ in Path(vaahai_test_dir).glob('**/__pycache__/**'))}")
    print(f"- Files with updated imports: {len(modified_files)}")
    
    print("\nNext steps:")
    print("1. Run the tests to verify everything works: poetry run pytest")
    print("2. Review the merged test directory structure")
    print("3. Once verified, remove the old test directory: rm -rf vaahai/test")
    print("4. Update any CI/CD configurations if needed")


if __name__ == "__main__":
    main()
