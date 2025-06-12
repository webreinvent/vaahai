#!/usr/bin/env python
"""Framework/CMS Detection Agent Example

Demonstrates how to use FrameworkDetectionAgent to detect technologies used in a
project directory.
"""
from pathlib import Path
import sys

# Ensure project root on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vaahai.agents.applications.framework_detection import FrameworkDetectionAgent


def main(project_dir: str):
    agent = FrameworkDetectionAgent({"name": "FrameworkDetector"})
    result = agent.run(project_dir)

    print("Framework/CMS Detection Result:\n===============================")
    print(f"Primary framework: {result['primary_framework']['name']} (confidence {result['primary_framework']['confidence']:.2f})")

    if result["secondary_frameworks"]:
        print("Secondary frameworks:")
        for fw in result["secondary_frameworks"]:
            print(f"  - {fw['name']} ({fw['confidence']:.2f})")

    print(f"CMS: {result['cms']['name']} (confidence {result['cms']['confidence']:.2f})")
    print("\nExplanation:")
    print(result["explanation"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: framework_detection_example.py <project_path>")
        sys.exit(1)
    main(sys.argv[1])
