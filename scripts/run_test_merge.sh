#!/bin/bash

# Script to install pytest-cov and run the test directory merge

set -e  # Exit on error

echo "=== Installing pytest-cov package ==="
poetry add pytest-cov --group dev

echo "=== Running test directory merge script ==="
python scripts/merge_test_directories.py

echo "=== Running tests to verify the merge ==="
poetry run pytest -v

echo "=== Test directory merge complete ==="
echo "If all tests pass, you can remove the old test directory with:"
echo "rm -rf vaahai/test"
