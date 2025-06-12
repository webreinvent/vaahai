#!/usr/bin/env python3
"""
Test file with various code issues for testing the review command.
"""

def example_function(username, password):
    """Example function with various code issues."""
    # This line is way too long and exceeds the default maximum line length of 100 characters by quite a bit, which should trigger the LineLength review step
    
    # Hardcoded API key (security issue)
    api_key = "sk-1234567890abcdef1234567890abcdef"
    
    # SQL injection vulnerability (security issue)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    # Inconsistent indentation (style issue)
    if True:
        print("Properly indented")
    if True:
            print("Improperly indented")
    
    # Inefficient loop - modifying list while iterating (performance issue)
    data = [1, 2, 3, -1, -2, 4, 5]
    for item in data:
        if item < 0:
            data.remove(item)
    
    # Large memory usage - reading entire file into memory (performance issue)
    with open('large_file.txt', 'r') as f:
        content = f.read()
    
    return data
