#!/usr/bin/env python3
"""
Example script demonstrating the VaahAI Tool Registry.

This script shows how to use the tool registry, factory, and pipeline components
to analyze code using different tools.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

from vaahai.tools.base import ToolRegistry, ToolFactory
from vaahai.tools.utils.pipeline import ToolPipeline
# Import tool implementations to ensure they are registered
from vaahai.tools.impl.code_linter import CodeLinterTool
from vaahai.tools.impl.static_analyzer import StaticAnalyzerTool


def main():
    """Run the tool registry example."""
    print("VaahAI Tool Registry Example")
    print("============================\n")
    
    # List available tools
    print("Available tools:")
    tools = ToolFactory.list_available_tools()
    for tool_type in tools:
        metadata = ToolFactory.get_tool_metadata(tool_type)
        print(f"  - {tool_type}: {metadata.get('description', 'No description')}")
        print(f"    Input: {metadata.get('input_type', 'unknown')}, Output: {metadata.get('output_type', 'unknown')}")
        print(f"    Tags: {', '.join(metadata.get('tags', []))}")
        print()
    
    # Filter tools by tag
    print("Tools with 'code_quality' tag:")
    quality_tools = ToolRegistry.get_tools_by_tag("code_quality")
    for tool_type in quality_tools:
        print(f"  - {tool_type}")
    print()
    
    # Filter tools by input type
    print("Tools that accept 'code' input:")
    code_tools = ToolRegistry.get_tools_by_input_type("code")
    for tool_type in code_tools:
        print(f"  - {tool_type}")
    print()
    
    # Filter tools by output type
    print("Tools that produce 'analysis_results' output:")
    analysis_tools = ToolRegistry.get_tools_by_output_type("analysis_results")
    for tool_type in analysis_tools:
        print(f"  - {tool_type}")
    print()
    
    # Create a code linter tool
    print("Creating a code linter tool...")
    linter_config = {
        "type": "code_linter",
        "severity_levels": ["error", "warning"],
        "ignore_patterns": ["# noqa"]
    }
    linter = ToolFactory.create_tool("code_linter", linter_config)
    
    # Sample Python code to analyze
    sample_code = """
import os
from glob import *  # Wildcard import

def process_files():
    # TODO: Implement file processing
    files = os.listdir('.')
    for file in files:
        print(file)  # Print statement
        
    # FIXME: Handle errors properly
    try:
        process_data()
    except:  # Bare except clause
        pass
        
def process_data():
    global data  # Global variable
    data = []
    exec("data.append(1)")  # Use of exec
    """
    
    # Run the linter
    print("Running code linter...")
    lint_results = linter.execute(sample_code)
    
    # Display results
    print("\nLint Results:")
    print(f"Total issues: {lint_results['summary']['total']}")
    print(f"Issues by severity: {lint_results['summary']['by_severity']}")
    print("\nDetailed issues:")
    for issue in lint_results["issues"]:
        print(f"  Line {issue['line']}: {issue['message']} ({issue['severity']})")
        print(f"    {issue['code']}")
    print()
    
    # Create a static analyzer tool
    print("Creating a static analyzer tool...")
    analyzer_config = {
        "type": "static_analyzer",
    }
    analyzer = ToolFactory.create_tool("static_analyzer", analyzer_config)
    
    # Run the analyzer
    print("Running static analyzer...")
    analysis_results = analyzer.execute(sample_code)
    
    # Display results
    print("\nAnalysis Results:")
    print(f"Language: {analysis_results['language']}")
    print(f"Metrics:")
    for key, value in analysis_results['metrics'].items():
        print(f"  {key}: {value}")
    
    print("\nImports:")
    for imp in analysis_results["imports"]:
        print(f"  - {imp}")
    
    print("\nFunctions:")
    for func in analysis_results["functions"]:
        print(f"  - {func['name']} (line {func['line']})")
    print()
    
    # Creating a tool pipeline
    print("Creating a tool pipeline...")
    # Note: In a real pipeline, we would ensure the output type of one tool
    # matches the input type of the next tool. For this example, we'll use
    # the tools independently since their input/output types don't match.
    
    # First tool: code linter
    print("Running code linter in pipeline...")
    linter_results = linter.execute(sample_code)
    print("\nLint Results Summary:")
    print(f"Total issues: {linter_results['summary']['total']}")
    print(f"Issues by severity: {linter_results['summary']['by_severity']}")
    
    # Second tool: static analyzer (run independently)
    print("\nRunning static analyzer in pipeline...")
    analyzer_results = analyzer.execute(sample_code)
    print("\nAnalysis Results Summary:")
    print(f"Language: {analyzer_results['language']}")
    print(f"Lines of code: {analyzer_results['metrics']['lines_of_code']}")
    print(f"Functions: {len(analyzer_results['functions'])}")
    print(f"Imports: {len(analyzer_results['imports'])}")
    
    print("\nExample complete!")
    
    # Create and run a tool pipeline
    # print("Creating a tool pipeline...")
    # pipeline_config = [
    #     {
    #         "type": "code_linter",
    #         "severity_levels": ["error"]
    #     },
    #     {
    #         "type": "static_analyzer"
    #     }
    # ]
    
    # tools = ToolFactory.create_tool_pipeline(pipeline_config)
    # pipeline = ToolPipeline(tools)
    
    # print("Running tool pipeline...")
    # pipeline_results = pipeline.execute(sample_code)
    
    # print("\nPipeline Results:")
    # print(f"Number of steps: {len(pipeline_results['pipeline_results'])}")
    
    # # Display the final output (static analyzer results)
    # final_output = pipeline_results["final_output"]
    # print(f"Final output: {final_output['language']} code analysis")
    # print(f"Functions found: {len(final_output['functions'])}")
    # print(f"Classes found: {len(final_output['classes'])}")
    
    # # Show how many errors were found by the linter (first step)
    # linter_output = pipeline_results["pipeline_results"][0]["output"]
    # error_count = linter_output["summary"]["by_severity"].get("error", 0)
    # print(f"Errors found by linter: {error_count}")


if __name__ == "__main__":
    main()
