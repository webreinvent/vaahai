#!/usr/bin/env python
"""
Language Detection Example

This script demonstrates how to use the LanguageDetectionAgent to detect
programming languages from code samples.
"""

import os
import sys
from pathlib import Path

# Add project root to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from vaahai.agents.applications.language_detection import LanguageDetectionAgent

def main():
    """Run language detection examples."""
    print("VaahAI Language Detection Agent Example")
    print("======================================\n")
    
    # Initialize the agent
    agent = LanguageDetectionAgent({"name": "LanguageDetector"})
    
    # Example code snippets
    examples = {
        "Python": """
import os
import sys

def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
""",
        "JavaScript": """
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
""",
        "Java": """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
""",
        "Ruby": """
#!/usr/bin/env ruby

class HelloWorld
  def initialize(name)
    @name = name
  end
  
  def greet
    puts "Hello, #{@name}!"
  end
end

hello = HelloWorld.new("World")
hello.greet
""",
        "Go": """
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
"""
    }
    
    # Test each example
    for language, code in examples.items():
        print(f"\nTesting {language} code detection:")
        print("-" * 40)
        result = agent.run(code)
        
        print(f"Detected primary language: {result['primary_language']['name']} " +
              f"(confidence: {result['primary_language']['confidence']:.2f})")
        
        if result.get('secondary_languages'):
            print("Secondary languages detected:")
            for lang in result['secondary_languages']:
                print(f"  - {lang['name']} (confidence: {lang['confidence']:.2f})")
        
        print(f"Explanation: {result.get('explanation', 'No explanation provided')}")
        print()
    
    # Test with file path
    print("\nTesting detection with file path:")
    print("-" * 40)
    
    # Create a temporary Python file
    temp_file = "temp_example.py"
    with open(temp_file, "w") as f:
        f.write(examples["Python"])
    
    try:
        result = agent.run(examples["Python"], file_path=temp_file)
        print(f"Detected primary language: {result['primary_language']['name']} " +
              f"(confidence: {result['primary_language']['confidence']:.2f})")
        print(f"Explanation: {result.get('explanation', 'No explanation provided')}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    main()
