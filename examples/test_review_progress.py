"""
Test file for demonstrating the review progress tracking feature.

This file contains various code patterns that will trigger different review steps,
allowing us to see the progress tracking in action.
"""

import os
import sqlite3
import time


def insecure_sql_query(user_input):
    """Example of an insecure SQL query that will trigger the SQLInjection step."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # This is insecure and will trigger the SQLInjection review step
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return results


def hardcoded_secrets():
    """Example of hardcoded secrets that will trigger the HardcodedSecrets step."""
    # These will trigger the HardcodedSecrets review step
    api_key = "1234567890abcdef1234567890abcdef"
    password = "super_secret_password123"
    
    # Using the secrets in some way
    return f"API Key: {api_key}, Password: {password}"


def inefficient_loop_example():
    """Example of inefficient loops that will trigger the InefficientLoops step."""
    # This will trigger the InefficientLoops review step
    items = [1, 2, 3, 4, 5]
    
    # Modifying a list while iterating over it
    for i in range(len(items)):
        if items[i] % 2 == 0:
            items.pop(i)  # This is problematic
    
    # Nested loops on the same iterable
    result = []
    for i in items:
        for j in items:
            result.append(i * j)
    
    return result


def large_memory_usage():
    """Example of code that uses large amounts of memory."""
    # This will trigger the LargeMemoryUsage review step
    
    # Reading an entire file into memory
    with open(__file__, "r") as f:
        content = f.read()
    
    # Large list comprehension
    large_list = [i * j for i in range(1000) for j in range(1000)]
    
    return len(content) + len(large_list)


def long_line_example():
    """Example of a very long line that will trigger the LineLength step."""
    # This line is very long and will trigger the LineLength review step
    return "This is a very long line that exceeds the recommended line length limit and will trigger the LineLength review step. It contains a lot of unnecessary text just to make it longer."


def inconsistent_indentation():
    """Example of inconsistent indentation that will trigger the IndentationConsistency step."""
    # This will trigger the IndentationConsistency review step
    if True:
        print("This is properly indented")
       print("This is not properly indented")  # Inconsistent indentation
    
    return "Done"


def main():
    """Run all the example functions."""
    print("Running examples...")
    
    try:
        insecure_sql_query("test_user")
    except Exception as e:
        print(f"SQL error: {e}")
    
    hardcoded_secrets()
    inefficient_loop_example()
    
    try:
        large_memory_usage()
    except Exception as e:
        print(f"Memory error: {e}")
    
    long_line_example()
    
    try:
        inconsistent_indentation()
    except Exception as e:
        print(f"Indentation error: {e}")
    
    print("Examples completed.")


if __name__ == "__main__":
    main()
