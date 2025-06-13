"""
Code change manager for applying suggested code changes.

This module provides utilities for safely applying suggested code changes
to original files with backup and validation functionality.
"""

import os
import shutil
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class CodeChangeManager:
    """
    Manages the application of code changes to files.
    
    This class handles the safe application of suggested code changes to original
    files, including creating backups and validating changes before applying them.
    """
    
    def __init__(self):
        """Initialize the code change manager."""
        self.backup_dir = os.path.expanduser("~/.vaahai/backups")
        self.changes_applied = []
        self.changes_rejected = []
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def backup_file(self, file_path: str) -> str:
        """
        Create a backup of the specified file.
        
        Args:
            file_path: Path to the file to back up
            
        Returns:
            Path to the backup file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot backup non-existent file: {file_path}")
            
        # Create a timestamped backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_path = os.path.join(
            self.backup_dir, 
            f"{filename}.{timestamp}.bak"
        )
        
        # Create the backup
        shutil.copy2(file_path, backup_path)
        
        return backup_path
    
    def apply_change(self, file_path: str, line_number: int, 
                    original_code: str, suggested_code: str) -> bool:
        """
        Apply a suggested code change to a file.
        
        Args:
            file_path: Path to the file to modify
            line_number: Line number where the change starts
            original_code: Original code snippet
            suggested_code: Suggested code snippet
            
        Returns:
            True if the change was applied successfully, False otherwise
        """
        if not os.path.exists(file_path):
            return False
            
        try:
            # Create a backup first
            backup_path = self.backup_file(file_path)
            
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Validate that the original code matches what's in the file
            original_lines = original_code.splitlines()
            file_lines = lines[line_number-1:line_number-1+len(original_lines)]
            file_content = ''.join(file_lines)
            
            # Strip whitespace for comparison
            if file_content.strip() != original_code.strip():
                # Original code doesn't match the file content
                return False
            
            # Replace the lines with the suggested code
            suggested_lines = suggested_code.splitlines(True)  # Keep line endings
            lines[line_number-1:line_number-1+len(original_lines)] = suggested_lines
            
            # Write the modified content back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            # Record the applied change
            self.changes_applied.append({
                'file_path': file_path,
                'line_number': line_number,
                'backup_path': backup_path
            })
            
            return True
            
        except Exception as e:
            # If anything goes wrong, try to restore from backup
            if 'backup_path' in locals() and os.path.exists(backup_path):
                shutil.copy2(backup_path, file_path)
            return False
    
    def reject_change(self, file_path: str, line_number: int) -> None:
        """
        Record a rejected code change.
        
        Args:
            file_path: Path to the file
            line_number: Line number where the change would have started
        """
        self.changes_rejected.append({
            'file_path': file_path,
            'line_number': line_number
        })
    
    def get_summary(self) -> Dict:
        """
        Get a summary of applied and rejected changes.
        
        Returns:
            Dictionary containing summary information
        """
        return {
            'applied': len(self.changes_applied),
            'rejected': len(self.changes_rejected),
            'applied_changes': self.changes_applied,
            'rejected_changes': self.changes_rejected
        }
