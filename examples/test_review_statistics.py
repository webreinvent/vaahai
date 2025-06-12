"""
Example file to demonstrate the review statistics collector feature.

This file contains various code patterns that will trigger different review steps,
allowing us to test the statistics collection functionality.
"""

import os
import sys
import sqlite3
import subprocess
from typing import List, Dict, Any


# Security issues - SQL Injection
def unsafe_query(user_input: str) -> List[Dict[str, Any]]:
    """Execute an unsafe SQL query with user input."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return results


# Security issues - Command Injection
def run_command(command: str) -> str:
    """Execute a shell command with user input."""
    # Command injection vulnerability
    result = os.system(command)
    return f"Command executed with status: {result}"


# Performance issues - Inefficient loops
def inefficient_loop(items: List[int]) -> List[int]:
    """Demonstrate inefficient loop patterns."""
    # Modifying list during iteration
    result = []
    for i in range(len(items)):
        if items[i] % 2 == 0:
            items.pop(i)  # This will cause issues
        else:
            result.append(items[i])
    
    # Nested loops with same iterable
    for i in range(len(result)):
        for j in range(len(result)):
            if result[i] == result[j] and i != j:
                print(f"Duplicate found: {result[i]}")
    
    return result


# Performance issues - Large memory usage
def read_large_file(file_path: str) -> str:
    """Read a large file inefficiently."""
    # Reading entire file into memory
    with open(file_path, "r") as f:
        content = f.read()  # Could cause memory issues with large files
    
    return content


# Style issues - Complex function
def complex_function(a: int, b: int, c: int, d: int, e: int, f: int, g: int) -> int:
    """A complex function with too many parameters and nested conditions."""
    result = 0
    
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        if f > 0:
                            if g > 0:
                                result = a + b + c + d + e + f + g
                            else:
                                result = a + b + c + d + e + f
                        else:
                            result = a + b + c + d + e
                    else:
                        result = a + b + c + d
                else:
                    result = a + b + c
            else:
                result = a + b
        else:
            result = a
    
    return result


# Style issues - Long function
def long_function():
    """A very long function that should be broken down."""
    print("This is the start of a very long function")
    
    # Lots of code here...
    for i in range(100):
        print(f"Step {i}")
        for j in range(100):
            if i * j % 10 == 0:
                print(f"Multiple of 10: {i * j}")
    
    # More code...
    result = 0
    for i in range(1000):
        result += i
    
    print(f"Final result: {result}")
    
    # Even more code...
    data = {}
    for i in range(100):
        data[f"key_{i}"] = f"value_{i}"
    
    return data


# Maintainability issues - Duplicate code
def calculate_area_circle(radius: float) -> float:
    """Calculate the area of a circle."""
    return 3.14159 * radius * radius


def calculate_area_circle_again(radius: float) -> float:
    """Calculate the area of a circle again."""
    # Duplicate code
    return 3.14159 * radius * radius


# Maintainability issues - Magic numbers
def calculate_tax(amount: float) -> float:
    """Calculate tax on an amount."""
    # Magic numbers
    if amount < 10000:
        return amount * 0.1
    elif amount < 50000:
        return amount * 0.2
    else:
        return amount * 0.3


# Best practice issues - Unused imports
def unused_imports_function():
    """Function with unused imports."""
    # sys and subprocess are imported but not used
    print("Hello world")


if __name__ == "__main__":
    print("Running example code to test review statistics collector...")
    
    # This will trigger various review steps and generate statistics
    unsafe_query("user' OR '1'='1")
    run_command("ls -la")
    inefficient_loop([1, 2, 3, 4, 5])
    
    try:
        read_large_file("large_file.txt")
    except FileNotFoundError:
        print("Large file not found, skipping...")
    
    complex_function(1, 2, 3, 4, 5, 6, 7)
    long_function()
    
    area1 = calculate_area_circle(5)
    area2 = calculate_area_circle_again(5)
    
    tax = calculate_tax(25000)
    
    unused_imports_function()
    
    print("Example code execution completed.")
