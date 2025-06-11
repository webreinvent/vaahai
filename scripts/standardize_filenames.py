#!/usr/bin/env python3
"""
Script to standardize file names to snake_case and update references.
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def to_snake_case(name: str) -> str:
    """Convert a string to snake_case while preserving file extensions."""
    # Skip if already in snake_case
    if name == name.lower():
        return name
        
    # Split into base and extension
    base, ext = os.path.splitext(name)
    
    # Convert base to snake_case
    # Handle camelCase and PascalCase
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', base)
    # Handle lowercase letters followed by uppercase letters
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    # Replace spaces and hyphens with underscores
    s3 = s2.replace('-', '_').replace(' ', '_')
    # Remove any remaining non-alphanumeric/underscore characters
    base_snake = re.sub(r'[^a-z0-9_]', '_', s3)
    
    # Recombine with original extension
    return f"{base_snake}{ext}" if ext else base_snake

def find_files_to_rename(directory: str) -> List[Tuple[str, str]]:
    """Find files that need to be renamed to snake_case."""
    to_rename = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == to_snake_case(file):
                continue
            old_path = os.path.join(root, file)
            new_file = to_snake_case(file)
            new_path = os.path.join(root, new_file)
            to_rename.append((old_path, new_path))
    return to_rename

def update_file_references(old_name: str, new_name: str, root_dir: str) -> None:
    """Update references to a file throughout the codebase."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.toml', '.yaml', '.yml')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Skip binary files
                    if '\x00' in content:
                        continue
                        
                    if old_name in content:
                        new_content = content.replace(old_name, new_name)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except (UnicodeDecodeError, PermissionError) as e:
                    print(f"Skipping {file_path}: {e}")

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Directories to process
    directories = [
        os.path.join(project_root, 'ai_docs'),
        os.path.join(project_root, 'specs'),
        os.path.join(project_root, 'docs'),
        os.path.join(project_root, 'ai_prompts'),
        # Add other directories if needed
    ]
    
    # First, collect all files to rename
    rename_pairs = []
    for directory in directories:
        if os.path.exists(directory):
            rename_pairs.extend(find_files_to_rename(directory))
    
    if not rename_pairs:
        print("No files need to be renamed.")
        return
    
    # Show planned changes
    print("The following files will be renamed:")
    for old, new in rename_pairs:
        print(f"  {old} -> {os.path.basename(new)}")
    
    # Auto-confirm for non-interactive use
    print("\nAuto-confirming renaming...")
    
    # Rename files and update references
    for old_path, new_path in rename_pairs:
        try:
            # Update references first
            update_file_references(
                os.path.basename(old_path),
                os.path.basename(new_path),
                project_root
            )
            # Then rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")

if __name__ == "__main__":
    main()
