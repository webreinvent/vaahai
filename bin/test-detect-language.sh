#!/bin/bash

# Test script for the vaahai detect-language command
# This script runs a series of tests to verify that the command is working correctly

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Testing vaahai detect-language command...${NC}"
echo

# Test 1: Help message
echo -e "${YELLOW}Test 1: Help message${NC}"
"$SCRIPT_DIR/vaahai-detect-language-script" --help
echo

# Test 2: Single file analysis
echo -e "${YELLOW}Test 2: Single file analysis${NC}"
"$SCRIPT_DIR/vaahai-detect-language-script" "$PROJECT_ROOT/vaahai/__main__.py"
echo

# Test 3: Directory analysis
echo -e "${YELLOW}Test 3: Directory analysis (sample)${NC}"
"$SCRIPT_DIR/vaahai-detect-language-script" "$PROJECT_ROOT/vaahai/cli/commands" --format markdown
echo

# Test 4: JSON output
echo -e "${YELLOW}Test 4: JSON output${NC}"
"$SCRIPT_DIR/vaahai-detect-language-script" "$PROJECT_ROOT/vaahai/__main__.py" --format json
echo

# Test 5: No LLM mode
echo -e "${YELLOW}Test 5: No LLM mode${NC}"
"$SCRIPT_DIR/vaahai-detect-language-script" "$PROJECT_ROOT/vaahai/__main__.py" --no-llm
echo

# Test 6: Error handling (non-existent file)
echo -e "${YELLOW}Test 6: Error handling (non-existent file)${NC}"
"$SCRIPT_DIR/vaahai-detect-language-script" "$PROJECT_ROOT/non-existent-file.py"
echo

echo -e "${GREEN}All tests completed!${NC}"
echo
echo -e "${GREEN}To install the command, run:${NC}"
echo "  $SCRIPT_DIR/install-detect-language.sh --local"
echo
echo -e "${GREEN}Then add to your PATH:${NC}"
echo "  export PATH=\"$PROJECT_ROOT/local/bin:\$PATH\""
echo
echo -e "${GREEN}You can then use the command as:${NC}"
echo "  vaahai detect-language path/to/file_or_directory"
