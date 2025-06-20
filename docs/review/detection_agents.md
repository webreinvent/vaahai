# Detection Agents in VaahAI

This document describes the detection agents used in VaahAI for identifying programming languages, frameworks, and content management systems (CMS) from code.

## LLMLanguageFrameworkCMSDetectionAgent

The `LLMLanguageFrameworkCMSDetectionAgent` is a unified detection agent that leverages Large Language Models (LLMs) to detect the programming language, framework, and CMS from code content. This agent replaces the previous separate language and framework detection agents with a single, more powerful solution.

### Features

- **Unified Detection**: Detects language, framework, and CMS in a single operation
- **Confidence Scores**: Provides confidence scores for each detection
- **Autogen Integration**: Fully compatible with the Microsoft Autogen framework
- **Fallback Mechanisms**: Includes robust fallback handling for parsing errors
- **Configurable**: Uses the default LLM provider configured in VaahAI
- **Multi-Provider Support**: Works with OpenAI, Claude, Junie, and Ollama

### Usage

The agent can be used directly in your code:

```python
from vaahai.review.agents.detection import LLMLanguageFrameworkCMSDetectionAgent

# Create the agent
agent = LLMLanguageFrameworkCMSDetectionAgent({"name": "MyDetection"})

# Detect language, framework, and CMS from code content
code_content = """
def hello():
    print("Hello, world!")
"""
result = agent.run(code_content, file_path="example.py")

# Access the results
language = result["primary_language"]["name"]
language_confidence = result["primary_language"]["confidence"]
framework = result["primary_framework"]["name"]
framework_confidence = result["primary_framework"]["confidence"]
cms = result["primary_cms"]["name"]
cms_confidence = result["primary_cms"]["confidence"]
```

### Return Format

The agent returns a dictionary with the following structure:

```python
{
    "primary_language": {
        "name": str,  # Name of the detected language or "Unknown"
        "confidence": float  # Confidence score between 0.0 and 1.0
    },
    "primary_framework": {
        "name": str,  # Name of the detected framework or None
        "confidence": float  # Confidence score between 0.0 and 1.0
    },
    "primary_cms": {
        "name": str,  # Name of the detected CMS or None
        "confidence": float  # Confidence score between 0.0 and 1.0
    }
}
```

### Integration with CLI

The `LLMLanguageFrameworkCMSDetectionAgent` is integrated with the VaahAI CLI `review` command. When reviewing code, the agent automatically detects the language, framework, and CMS of the code being reviewed.

For individual files, the agent:
1. Reads the full file content for accurate detection
2. Analyzes both content and file extension for best results
3. Displays language, framework, and CMS with confidence scores

For directories, the agent:
1. Samples up to 5 representative files from the directory
2. Combines content from up to 3 files (limited to 1000 chars each) to stay within token limits
3. Skips hidden files and non-code files (images, PDFs, etc.)
4. Makes a collective determination of the project's technology stack

### Fallback Mechanisms

The CLI implements a robust fallback strategy:

1. If the unified detection agent fails:
   - Falls back to using separate `LanguageDetectionAgent` and `FrameworkDetectionAgent`
   - Reports what fallback mechanisms were activated (in debug mode)

2. If all detection attempts fail:
   - Uses file extension-based detection for common file types 
   - Reports "Unknown" for undetermined values
   - Continues with the review process regardless of detection results

### LLM Integration

The agent uses the VaahAI LLM client utility system for provider integration:

1. **Provider Selection**: Uses the default LLM provider set in VaahAI config
2. **API Key Management**: Securely retrieves API keys from configuration or environment variables
3. **Model Selection**: Uses provider-specific default models with appropriate parameters
4. **Error Handling**: Includes comprehensive error handling and logging
5. **Supported Providers**:
   - OpenAI (GPT models)
   - Anthropic Claude
   - Junie
   - Ollama (local models)

The LLM client is implemented in `vaahai.utils.llm_client` and provides a unified interface for all supported providers.

## Legacy Detection Agents

For backward compatibility, VaahAI maintains the following legacy detection agents:

- `LanguageDetectionAgent`: Detects programming languages
- `FrameworkDetectionAgent`: Detects web frameworks and CMS

These agents are used as fallbacks if the unified detection agent fails.

## Example

See the `examples/llm_detection_example.py` script for a complete example of using the `LLMLanguageFrameworkCMSDetectionAgent`. The example demonstrates:

1. How to initialize the agent with proper configuration
2. How to use it with different code samples
3. How to interpret and display the results with confidence scores
4. Error handling and fallback patterns
