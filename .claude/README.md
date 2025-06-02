# Claude Command Prompts for Vaahai

This directory contains specialized command prompts for use with the Windsurf extension in PyCharm to streamline development of the Vaahai project, particularly focused on the Autogen multi-agent integration.

## Quick Start Guide

### Setup

1. Ensure you have the Windsurf extension installed in PyCharm
2. Open the Vaahai project in PyCharm
3. The `.claude` directory and its command prompts will be automatically recognized by the extension

### Using Command Prompts

1. Open the Windsurf sidebar in PyCharm
2. Navigate to the "Commands" section
3. Select a command prompt from the list
4. Click "Run Command" or use the keyboard shortcut (usually Alt+C)

Alternatively, you can:

1. Open any `.prompt` file from the `.claude/commands` directory
2. Click the "Run Prompt" button that appears in the editor
3. Claude will execute the command with the current context

## Available Commands

### Project Management

- **project_context.prompt**: Get a comprehensive overview of the Vaahai project architecture with Autogen integration
- **implementation_status.prompt**: Review current implementation status and next steps
- **update_implementation_status.prompt**: Update status documents after completing tasks
- **plan_next_task.prompt**: Plan the next implementation task with detailed steps

### Autogen Integration

- **autogen_agent_design.prompt**: Design and implement a specialized Autogen agent
- **test_autogen_agent.prompt**: Test a specific Autogen agent with code samples
- **configure_autogen_system.prompt**: Configure the multi-agent system settings
- **create_prompt_templates.prompt**: Create comprehensive prompt templates for agents

### Documentation

- **update_docs.prompt**: Audit and update documentation across the project
- **test_strategy.prompt**: Develop a testing strategy for Autogen integration

### Code Quality

- **code_review.prompt**: Get a comprehensive code review
- **fix_suggestion.prompt**: Get suggestions for fixing specific code issues
- **performance_optimization.prompt**: Analyze code for performance improvements
- **security_audit.prompt**: Perform a security audit on code

## Creating Custom Commands

To create a new command prompt:

1. Create a new file in the `.claude/commands` directory with a `.prompt` extension
2. Structure your prompt with clear instructions and placeholders
3. Save the file and it will automatically appear in the Windsurf commands list

## Best Practices

1. **Be Specific**: When using a command, provide specific details about what you're working on
2. **Include Context**: Reference relevant files, components, or requirements
3. **Use Variables**: Commands support variables like `{language}` or `{code}` that will be replaced with actual values
4. **Chain Commands**: For complex tasks, use multiple commands in sequence

## Example Workflow

1. Use **project_context.prompt** to get an overview of the project
2. Use **plan_next_task.prompt** to plan implementation of a specific agent
3. Use **autogen_agent_design.prompt** to design and implement the agent
4. Use **test_autogen_agent.prompt** to test the implementation
5. Use **update_implementation_status.prompt** to update project status

## Keyboard Shortcuts

- **Alt+C**: Run the current command
- **Alt+Shift+C**: Run the current command with custom parameters
- **Alt+P**: Open the command prompt selector

These shortcuts may vary based on your PyCharm keymap configuration.

## Troubleshooting

If you encounter issues with command prompts:

1. Ensure the Windsurf extension is up to date
2. Check that your prompt follows the expected format
3. Verify that any referenced files or paths exist
4. Try restarting PyCharm if commands aren't appearing

## Contributing

Feel free to add new command prompts or improve existing ones. When adding a new command:

1. Follow the established naming convention
2. Include clear instructions and examples
3. Document the command in this README
4. Test the command with different scenarios
