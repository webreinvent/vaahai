#!/usr/bin/env python3
"""
Example script demonstrating the VaahAI developer review command with enhanced diagnostics.

This script shows how to use the developer review command to analyze code with
detailed debugging information, timing statistics, and configuration validation.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Sample code with various issues for review
SAMPLE_CODE = """
import sqlite3
import os
import subprocess

# Security issue: SQL injection vulnerability
def get_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection vulnerability
    cursor.execute(query)
    return cursor.fetchone()

# Security issue: Hardcoded credentials
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
PASSWORD = "super_secret_password"

# Performance issue: Inefficient loop
def process_items(items):
    result = []
    for i in range(len(items)):  # Inefficient loop
        result.append(items[i] * 2)
    return result

# Security issue: Command injection vulnerability
def run_command(user_input):
    os.system(f"echo {user_input}")  # Command injection vulnerability
    return subprocess.check_output(f"ls {user_input}", shell=True)  # Another vulnerability
"""

def main():
    """Run the example script."""
    print("VaahAI Developer Review Command Example")
    print("======================================")
    
    # Create a temporary file with the sample code
    temp_file = project_root / "examples" / "sample_code_for_review.py"
    temp_file.write_text(SAMPLE_CODE)
    print(f"Created sample code file: {temp_file}")
    
    try:
        # Example 1: Basic developer review
        print("\n\nExample 1: Basic developer review")
        print("--------------------------------")
        cmd = ["vaahai", "dev", "review", "run", str(temp_file)]
        subprocess.run(cmd, check=True)
        
        # Example 2: Developer review with debug level
        print("\n\nExample 2: Developer review with debug level")
        print("----------------------------------------")
        cmd = ["vaahai", "dev", "review", "run", str(temp_file), "--debug-level", "debug"]
        subprocess.run(cmd, check=True)
        
        # Example 3: Developer review with step timing
        print("\n\nExample 3: Developer review with step timing")
        print("----------------------------------------")
        cmd = ["vaahai", "dev", "review", "run", str(temp_file), "--show-steps"]
        subprocess.run(cmd, check=True)
        
        # Example 4: Developer review with configuration display
        print("\n\nExample 4: Developer review with configuration display")
        print("-----------------------------------------------")
        cmd = ["vaahai", "dev", "review", "run", str(temp_file), "--show-config"]
        subprocess.run(cmd, check=True)
        
        # Example 5: Developer review with HTML output
        print("\n\nExample 5: Developer review with HTML output")
        print("----------------------------------------")
        cmd = ["vaahai", "dev", "review", "run", str(temp_file), "--format", "html"]
        subprocess.run(cmd, check=True)
        
        # Example 6: Developer review with trace level logging
        print("\n\nExample 6: Developer review with trace level logging")
        print("---------------------------------------------")
        cmd = ["vaahai", "dev", "review", "run", str(temp_file), "--debug-level", "trace"]
        subprocess.run(cmd, check=True)
        
    finally:
        # Clean up the temporary file
        if temp_file.exists():
            temp_file.unlink()
            print(f"\nCleaned up temporary file: {temp_file}")


if __name__ == "__main__":
    main()
