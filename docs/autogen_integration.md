# Autogen Framework Integration

This document outlines the architecture and implementation details for integrating Microsoft's Autogen framework into Vaahai to create a sophisticated multi-agent system for code review.

## Overview

Vaahai is integrating Autogen to leverage a multi-agent approach to code review, where specialized agents collaborate to provide comprehensive analysis of code. This approach allows for more sophisticated and thorough reviews by distributing different aspects of code analysis to specialized agents.

## Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────────────────────────────┐
│                    Review Coordinator Agent                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Group Chat Manager                       │
└───────┬───────────────┬────────────────┬────────────┬───────────┘
        │               │                │            │
        ▼               ▼                ▼            ▼
┌───────────┐   ┌───────────────┐  ┌──────────┐  ┌──────────────┐
│ Language  │   │ Framework/CMS │  │Standards │  │   Security   │
│ Detector  │   │   Detector    │  │ Analyzer │  │   Auditor    │
└───────────┘   └───────────────┘  └──────────┘  └──────────────┘
```

### Key Components

1. **Agent Factory**: Creates specialized agents based on configuration
2. **Review Orchestrator**: Manages the review process and agent collaboration
3. **Group Chat Manager**: Facilitates communication between agents
4. **Result Processor**: Processes and formats the results of the review

## Specialized Agents

### 1. Language Detector Agent

**Purpose**: Identify programming languages, features, and versions used in the code.

**Responsibilities**:
- Detect primary programming language(s)
- Identify language version indicators
- Recognize language-specific features and patterns

**Example Prompt**:
```
You are a Language Detector Agent specialized in identifying programming languages.
Analyze the following code and determine:
1. The primary programming language(s) used
2. Language version indicators if present
3. Any language-specific features or patterns

Code to analyze:
{code_snippet}
```

### 2. Framework/CMS Detector Agent

**Purpose**: Identify frameworks, libraries, and architectural patterns used in the code.

**Responsibilities**:
- Detect frameworks and libraries
- Identify architectural patterns (MVC, MVVM, etc.)
- Map dependencies and their relationships

**Example Prompt**:
```
You are a Framework Detector Agent specialized in identifying frameworks and libraries.
Analyze the following code and determine:
1. Frameworks or libraries being used
2. Architectural patterns (MVC, MVVM, etc.)
3. Key dependencies and their relationships

Code to analyze:
{code_snippet}
```

### 3. Standards Analyzer Agent

**Purpose**: Evaluate adherence to coding standards and best practices.

**Responsibilities**:
- Check adherence to language-specific coding standards
- Identify style inconsistencies
- Detect best practice violations

**Example Prompt**:
```
You are a Standards Analyzer Agent specialized in evaluating adherence to coding standards.
Analyze the following code and determine:
1. Adherence to language-specific coding standards
2. Style consistency issues
3. Best practice violations

Code to analyze:
{code_snippet}
```

### 4. Security Auditor Agent

**Purpose**: Identify security vulnerabilities and recommend improvements.

**Responsibilities**:
- Detect security vulnerabilities
- Identify common security anti-patterns
- Recommend security improvements

**Example Prompt**:
```
You are a Security Auditor Agent specialized in identifying security vulnerabilities.
Analyze the following code and determine:
1. Security vulnerabilities
2. Common security anti-patterns
3. Security best practice violations

Code to analyze:
{code_snippet}
```

### 5. Review Coordinator Agent

**Purpose**: Orchestrate the review process and aggregate findings.

**Responsibilities**:
- Divide code into logical segments
- Route specific questions to specialized agents
- Aggregate findings and generate a comprehensive report

**Example Prompt**:
```
You are a Review Coordinator Agent responsible for orchestrating the code review process.
Your tasks include:
1. Dividing code into logical segments
2. Routing specific questions to specialized agents
3. Aggregating findings and generating a comprehensive report

Code to review:
{code_snippet}
```

## Implementation Plan

### Phase 1: Setup

1. Add Autogen as a dependency
2. Create basic agent infrastructure
3. Implement agent configuration loading

### Phase 2: Agent Development

1. Implement specialized agents
2. Create prompt templates for each agent
3. Define agent capabilities and limitations

### Phase 3: Orchestration

1. Implement the coordinator agent
2. Define workflow between agents
3. Create fallback mechanisms

### Phase 4: Integration

1. Connect Autogen system to the CLI
2. Implement output formatting for agent results
3. Add configuration options for agent customization

## Configuration

### Agent Configuration Schema

```toml
[agents]
# Global agent settings
max_rounds = 10
termination_message = "REVIEW_COMPLETE"

[agents.language_detector]
name = "LanguageDetector"
model = "gpt-4"
temperature = 0.2
system_message = """You are a Language Detector Agent..."""

[agents.framework_detector]
name = "FrameworkDetector"
model = "gpt-4"
temperature = 0.3
system_message = """You are a Framework Detector Agent..."""

# Additional agent configurations...

[group_chat]
max_rounds = 10
speaker_selection_method = "auto"
```

## CLI Integration

The Autogen integration will be accessible through the existing `review` command with an additional `--agent-config` option to specify a custom agent configuration file:

```bash
vaahai review path/to/file.py --agent-config path/to/agent_config.toml
```

## Output Formats

The multi-agent system will support the same output formats as the current implementation:

1. **Terminal**: Rich terminal output with color coding
2. **Markdown**: Structured markdown for documentation
3. **HTML**: Web-friendly format with styling

## Future Enhancements

1. **Custom Agent Creation**: Allow users to define their own specialized agents
2. **Agent Memory**: Implement persistent memory for agents across reviews
3. **Multi-File Context**: Enable agents to understand relationships between multiple files
4. **Interactive Reviews**: Allow users to ask follow-up questions to specific agents
5. **Visualization**: Add visualization of agent collaboration and decision-making process
