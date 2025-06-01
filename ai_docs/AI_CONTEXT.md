# You are an expert python developer, ai agent developer, technical writer and software architect with expertise in Autogen Framework and CLI software development.

Write structured documentation which AI code generators can understand for the following requirement. Organize your response into logical sections such as Overview, Features, Technology Stack, CLI Specification, System Architecture & Flow, File/Module Structure, Extensibility, Example AI Prompt, Example Output, Tool Configuration, Installation & Usage, and Implementation Snippets.

## Provide a detailed plan to develop this project, started with an MVP. Each step must be test and working before moving to next step.

Create following directories with specified responsibilities:
/docs - To create project documentation who wants to use this software, like get started, installation, how to use etc
/ai_docs - AI Coding tools persistent memory. A knowledge repository for AI tools can instantly access. It will contain API docs & integrations, Architecture docs / design docs, Hidden non-code business logic, Project-specific patterns
/specs - It will contain Project plan, Product Requirements Document, features etc. THIS IS THE FIRST DOCUMENT WE SHOULD PREPARE.
/.claude/commands - This directory will contain AI Prompts. Reusable prompts you can use with your ai tools. This reduces the time it takes to run repeat workflows in your codebases and in your ai tools. Although this is specific to Claude Code, the reusable prompts are not limited to any specific ai tooling.


## Command Line Tool Requirements:
- Develop a Python-based Command-Line Interface (CLI) tool that performs automated, AI-augmented code reviews using Microsoft’s AutoGen framework and large language models (LLMs) such as OpenAI GPT-4 (or a local LLM via Ollama). 
- It can accept folders, files, model etc as arguments
- Tool can run static analysis (e.g., pylint, flake8, bandit, php, laravel, nuxt, vue, etc), aggregate the findings for prompt construction, and generate an AI-powered, context-aware code review through the LLM. Present reviews in the terminal
- Option to apply the change one by one, by asking for confirmation. 
- Organize the code in modules for CLI, static analysis integration, AI agent handling (via AutoGen), configuration, formatting, and utilities. 
- Allow user configuration for LLM API keys, review preferences, and output options through command-line config commands.


## Preferred Tools & Stack:

Programming Language: Python
CLI Framework: Typer or Click
Static Analysis: pylint, flake8, bandit
AI Agent Orchestration: Microsoft AutoGen
LLM: OpenAI GPT-4 (API) or local LLM via Ollama
Output: Terminal, Markdown, HTML (via Python libraries) or apply code changes directly in files
Config: JSON or TOML-based file in user home directory
Packaging: Poetry or setuptools

## Documentation Must Include:

- Concise overview of purpose and features
- Technology stack table/list with justifications
- Specific CLI commands, usage scenarios, and options
- Architectural diagram or structured flow section
- Example module/file structure
- Guidelines for customization/extensibility
- Example of an AI prompt used in reviews
- Example of review output (Markdown sample)
- Configuration and installation instructions
- Implementation tips or code snippets
- Write in clear, professional language


## Audience:

Python developers
Open-source contributors
AI code generation tools

## Goal:
- Make it easy for AI code generators and developers to generate all needed scaffolding, modules, and future extensions.
- Be explicit, structured, and comprehensive.
- Respond with the complete documentation only.

NOTE: YOU ONLY NEED TO GENERATE THE DOCUMENTATION OF AI CONTEXT