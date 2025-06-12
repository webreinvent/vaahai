#!/usr/bin/env python3
"""
Example script demonstrating the usage of the VaahAI review steps system.

This script shows how to:
1. List all registered review steps
2. Filter review steps by category
3. Create and execute review step instances
4. Validate review step configurations
5. Use the ReviewRunner to run multiple steps at once
"""

import json
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from vaahai.review import (
    ReviewStep,
    ReviewStepCategory,
    ReviewStepSeverity,
    ReviewStepRegistry,
    validate_step_config,
    ReviewRunner,
    
    # Built-in review steps
    LineLength,
    IndentationConsistency,
    HardcodedSecrets,
    SQLInjection,
    InefficientLoops,
    LargeMemoryUsage,
)


def print_separator(title):
    """Print a separator with a title."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")


def list_all_steps():
    """List all registered review steps."""
    print_separator("All Registered Review Steps")
    
    all_steps = ReviewStepRegistry.get_all_steps()
    print(f"Found {len(all_steps)} registered review steps:\n")
    
    for step_id, step_class in all_steps.items():
        print(f"- {step_id}: {step_class.__name__}")
    
    return all_steps


def filter_steps_by_category():
    """Filter review steps by category."""
    print_separator("Filtering Review Steps by Category")
    
    # Filter style steps
    style_steps = ReviewStepRegistry.filter_steps(category=[ReviewStepCategory.STYLE])
    print(f"Found {len(style_steps)} style review steps:")
    for step_id in style_steps:
        print(f"- {step_id}")
    
    # Filter security steps
    security_steps = ReviewStepRegistry.filter_steps(category=[ReviewStepCategory.SECURITY])
    print(f"\nFound {len(security_steps)} security review steps:")
    for step_id in security_steps:
        print(f"- {step_id}")
    
    # Filter performance steps
    performance_steps = ReviewStepRegistry.filter_steps(category=[ReviewStepCategory.PERFORMANCE])
    print(f"\nFound {len(performance_steps)} performance review steps:")
    for step_id in performance_steps:
        print(f"- {step_id}")


def execute_style_steps():
    """Execute style review steps on sample code."""
    print_separator("Executing Style Review Steps")
    
    # Sample code with style issues
    code = """
def example_function():
    # This line is way too long and exceeds the default maximum line length of 79 characters by quite a bit
    
    # Inconsistent indentation
    x = 1
	y = 2  # This line uses a tab for indentation
    z = 3  # This line uses spaces for indentation
    return x + y + z
"""
    
    print("Sample code with style issues:")
    print(code)
    
    # Create and execute the LineLength review step
    line_length_step = LineLength()
    line_length_result = line_length_step.execute({"content": code, "file_path": "example.py"})
    
    print("\nLineLength review step results:")
    print(f"Status: {line_length_result['status']}")
    print(f"Message: {line_length_result['message']}")
    print("Issues:")
    for issue in line_length_result["issues"]:
        print(f"- Line {issue['line']}: {issue['message']}")
    
    # Create and execute the IndentationConsistency review step
    indentation_step = IndentationConsistency()
    indentation_result = indentation_step.execute({"content": code, "file_path": "example.py"})
    
    print("\nIndentationConsistency review step results:")
    print(f"Status: {indentation_result['status']}")
    print(f"Message: {indentation_result['message']}")
    print("Issues:")
    for issue in indentation_result["issues"]:
        print(f"- Line {issue['line']}: {issue['message']}")


def execute_security_steps():
    """Execute security review steps on sample code."""
    print_separator("Executing Security Review Steps")
    
    # Sample code with security issues
    code = """
def authenticate_user(username, password):
    # Hardcoded API key (security issue)
    api_key = "sk-1234567890abcdef1234567890abcdef"
    
    # SQL injection vulnerability (security issue)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    return cursor.fetchone()
"""
    
    print("Sample code with security issues:")
    print(code)
    
    # Create and execute the HardcodedSecrets review step
    secrets_step = HardcodedSecrets()
    secrets_result = secrets_step.execute({"content": code, "file_path": "example.py"})
    
    print("\nHardcodedSecrets review step results:")
    print(f"Status: {secrets_result['status']}")
    print(f"Message: {secrets_result['message']}")
    print("Issues:")
    for issue in secrets_result["issues"]:
        print(f"- Line {issue['line']}: {issue['message']}")
    
    # Create and execute the SQLInjection review step
    sql_step = SQLInjection()
    sql_result = sql_step.execute({"content": code, "file_path": "example.py"})
    
    print("\nSQLInjection review step results:")
    print(f"Status: {sql_result['status']}")
    print(f"Message: {sql_result['message']}")
    print("Issues:")
    for issue in sql_result["issues"]:
        print(f"- Line {issue['line']}: {issue['message']}")


def execute_performance_steps():
    """Execute performance review steps on sample code."""
    print_separator("Executing Performance Review Steps")
    
    # Sample code with performance issues
    code = """
def process_data(data):
    # Inefficient loop - modifying list while iterating (performance issue)
    for item in data:
        if item < 0:
            data.remove(item)
    
    # Inefficient loop - using range(len()) instead of enumerate (performance issue)
    for i in range(len(data)):
        print(i, data[i])
    
    # Large memory usage - reading entire file into memory (performance issue)
    with open('large_file.txt', 'r') as f:
        content = f.read()
    
    # Large memory usage - nested list comprehension (performance issue)
    matrix = [[i*j for i in range(1000)] for j in range(1000)]
    
    return data
"""
    
    print("Sample code with performance issues:")
    print(code)
    
    # Create and execute the InefficientLoops review step
    loops_step = InefficientLoops()
    loops_result = loops_step.execute({"content": code, "file_path": "example.py"})
    
    print("\nInefficientLoops review step results:")
    print(f"Status: {loops_result['status']}")
    print(f"Message: {loops_result['message']}")
    print("Issues:")
    for issue in loops_result["issues"]:
        print(f"- Line {issue['line']}: {issue['message']}")
    
    # Create and execute the LargeMemoryUsage review step
    memory_step = LargeMemoryUsage()
    memory_result = memory_step.execute({"content": code, "file_path": "example.py"})
    
    print("\nLargeMemoryUsage review step results:")
    print(f"Status: {memory_result['status']}")
    print(f"Message: {memory_result['message']}")
    print("Issues:")
    for issue in memory_result["issues"]:
        print(f"- Line {issue['line']}: {issue['message']}")


def validate_step_configurations():
    """Validate review step configurations."""
    print_separator("Validating Review Step Configurations")
    
    # Valid LineLength configuration
    valid_config = {
        "max_length": 100,
    }
    
    # Invalid LineLength configuration (wrong type)
    invalid_config = {
        "max_length": "100",  # Should be an integer
    }
    
    # Validate the configurations
    print("Validating LineLength configuration:")
    
    print("\nValid configuration:")
    print(valid_config)
    try:
        # Use is_instance_config=True for instance configuration validation
        is_valid = validate_step_config("line_length", valid_config, is_instance_config=True)
        print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
    except Exception as e:
        print(f"Validation error: {e}")
    
    print("\nInvalid configuration:")
    print(invalid_config)
    try:
        # Use is_instance_config=True for instance configuration validation
        is_valid = validate_step_config("line_length", invalid_config, is_instance_config=True)
        print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
    except Exception as e:
        print(f"Validation error: {e}")


def use_review_runner():
    """Demonstrate using the ReviewRunner to run multiple steps at once."""
    print_separator("Using ReviewRunner")
    
    # Sample code with various issues
    code = """
def example_function():
    # This line is way too long and exceeds the default maximum line length of 79 characters by quite a bit
    
    # Hardcoded API key (security issue)
    api_key = "sk-1234567890abcdef1234567890abcdef"
    
    # SQL injection vulnerability (security issue)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    # Inefficient loop - modifying list while iterating (performance issue)
    for item in data:
        if item < 0:
            data.remove(item)
    
    # Large memory usage - reading entire file into memory (performance issue)
    with open('large_file.txt', 'r') as f:
        content = f.read()
    
    return data
"""
    
    print("Sample code with various issues:")
    print(code)
    
    # Create review step instances directly
    line_length_step = LineLength(max_length=100)
    hardcoded_secrets_step = HardcodedSecrets()
    
    # Create a ReviewRunner with specific step instances
    print("\nRunning specific review steps:")
    runner1 = ReviewRunner(steps=[line_length_step, hardcoded_secrets_step])
    result1 = runner1.run_on_content(code, "example.py")
    
    print(f"Status: {result1['status']}")
    print(f"Message: {result1['message']}")
    print(f"Total issues: {result1['total_issues']}")
    print("Results by step:")
    for step_result in result1["results"]:
        print(f"- {step_result['step_name']}: {len(step_result['issues'])} issues")
    
    # Create security review step instances
    sql_injection_step = SQLInjection()
    
    # Create a ReviewRunner with security steps
    print("\nRunning all security review steps:")
    runner2 = ReviewRunner(steps=[hardcoded_secrets_step, sql_injection_step])
    result2 = runner2.run_on_content(code, "example.py")
    
    print(f"Status: {result2['status']}")
    print(f"Message: {result2['message']}")
    print(f"Total issues: {result2['total_issues']}")
    print("Results by step:")
    for step_result in result2["results"]:
        print(f"- {step_result['step_name']}: {len(step_result['issues'])} issues")
    
    # Create performance review step instances
    inefficient_loops_step = InefficientLoops()
    large_memory_usage_step = LargeMemoryUsage()
    
    # Create a ReviewRunner with performance steps
    print("\nRunning all performance review steps:")
    runner3 = ReviewRunner(steps=[inefficient_loops_step, large_memory_usage_step])
    result3 = runner3.run_on_content(code, "example.py")
    
    print(f"Status: {result3['status']}")
    print(f"Message: {result3['message']}")
    print(f"Total issues: {result3['total_issues']}")
    print("Results by step:")
    for step_result in result3["results"]:
        print(f"- {step_result['step_name']}: {len(step_result['issues'])} issues")


def main():
    """Main function."""
    list_all_steps()
    filter_steps_by_category()
    execute_style_steps()
    execute_security_steps()
    execute_performance_steps()
    validate_step_configurations()
    use_review_runner()


if __name__ == "__main__":
    main()
