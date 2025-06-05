"""
VaahAI Report Generation Agent Implementation

This module provides the ReportGenerationAgent class, which specializes in
generating formatted reports and data visualizations.
"""

import logging
from typing import Dict, Any, List, Optional

from ...exceptions import AgentConfigurationError, AgentCommunicationError, ReportGenerationError, AgentMessageError
from .base import SpecializedAgent

logger = logging.getLogger(__name__)


class ReportGenerationAgent(SpecializedAgent):
    """
    A specialized agent for report generation.
    
    ReportGenerationAgent extends SpecializedAgent with capabilities specific to
    report generation, such as data formatting, visualization, and summarization.
    """
    
    def __init__(self, agent_id: Optional[str] = None, name: Optional[str] = None):
        """
        Initialize a new report generation agent.
        
        Args:
            agent_id: Unique identifier for this agent. If not provided, a UUID will be generated.
            name: Display name for this agent. If not provided, the class name will be used.
        """
        super().__init__(agent_id, name or "ReportGenerator")
        self._report_formats: List[str] = []
        self._visualization_types: List[str] = []
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the agent with the provided configuration.
        
        Args:
            config: Configuration dictionary for the agent
            
        Returns:
            True if initialization was successful, False otherwise
        """
        # Update the agent name if provided in the config
        if 'name' in config and isinstance(config['name'], str):
            self._name = config['name']
        
        # Continue with normal initialization
        return super().initialize(config)
    
    def _validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if the configuration is valid, False otherwise
            
        Raises:
            AgentConfigurationError: If the configuration is invalid
        """
        # First validate using parent class validation
        try:
            if not super()._validate_config():
                return False
        except Exception as e:
            # Re-raise with more context
            raise AgentConfigurationError(self._name, "base_config", str(e))
        
        # Validate report formats if provided
        if 'report_formats' in self._config:
            if not isinstance(self._config['report_formats'], list):
                error_msg = "report_formats must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "report_formats", error_msg)
            
            for format_type in self._config['report_formats']:
                if not isinstance(format_type, str):
                    error_msg = "each report format must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "report_formats", error_msg)
            
            self._report_formats = self._config['report_formats']
        else:
            logger.info(f"No report formats specified for {self._name}, using default formats")
            self._report_formats = ["markdown", "html", "plain_text"]
        
        # Validate visualization types if provided
        if 'visualization_types' in self._config:
            if not isinstance(self._config['visualization_types'], list):
                error_msg = "visualization_types must be a list"
                logger.error(error_msg)
                raise AgentConfigurationError(self._name, "visualization_types", error_msg)
            
            for viz_type in self._config['visualization_types']:
                if not isinstance(viz_type, str):
                    error_msg = "each visualization type must be a string"
                    logger.error(error_msg)
                    raise AgentConfigurationError(self._name, "visualization_types", error_msg)
            
            self._visualization_types = self._config['visualization_types']
        else:
            logger.info(f"No visualization types specified for {self._name}, using default types")
            self._visualization_types = ["bar_chart", "line_graph", "pie_chart", "table"]
        
        return True
    
    def _initialize_capabilities(self) -> None:
        """
        Initialize the agent's capabilities based on configuration.
        """
        # Initialize parent capabilities
        super()._initialize_capabilities()
        
        # Add report generation capabilities
        self.add_capability('report_generation')
        self.add_capability('data_visualization')
        
        # Add format-specific capabilities
        for format_type in self._report_formats:
            self.add_capability(f"format_{format_type}")
        
        # Add visualization-specific capabilities
        for viz_type in self._visualization_types:
            self.add_capability(f"visualization_{viz_type}")
    
    def get_supported_formats(self) -> List[str]:
        """
        Get the list of report formats supported by this agent.
        
        Returns:
            List of supported format identifiers
        """
        return self._report_formats
    
    def get_visualization_types(self) -> List[str]:
        """
        Get the list of visualization types this agent can generate.
        
        Returns:
            List of visualization type identifiers
        """
        return self._visualization_types
    
    async def _generate_response(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a report based on the given message.
        
        Args:
            message: The message containing data and report specifications
            
        Returns:
            Report generation response message
            
        Raises:
            AgentMessageError: If the message format is invalid
            ReportGenerationError: If there is an error during report generation
        """
        try:
            # Validate message format
            if not isinstance(message, dict):
                raise AgentMessageError(self._name, "unknown", "Message must be a dictionary")
            
            message_type = message.get('type', 'unknown')
            
            # Check for required fields
            if 'data' not in message:
                raise AgentMessageError(
                    self._name,
                    message_type,
                    "Message must contain 'data' field for report generation"
                )
            
            data = message['data']
            if not isinstance(data, dict):
                raise AgentMessageError(
                    self._name,
                    message_type,
                    "Data must be a dictionary"
                )
            
            # Get report format
            report_format = message.get('format', 'markdown')
            if report_format not in self._report_formats:
                raise ReportGenerationError(
                    self._name,
                    f"Unsupported report format: {report_format}",
                    format=report_format
                )
            
            # Get report title
            title = message.get('title', 'Generated Report')
            
            # In a real implementation, this would generate a proper report
            # For now, we return a placeholder response
            report_content = f"# {title}\n\n"
            report_content += "## Summary\n\n"
            report_content += "This is a placeholder report generated by the Report Generation Agent.\n\n"
            report_content += "## Data\n\n"
            
            # Add data items
            for key, value in data.items():
                report_content += f"- **{key}**: {value}\n"
            
            return {
                'type': 'report',
                'content': f"Report Generation Agent {self._name} has generated a report: '{title}'",
                'sender': self._name,
                'recipient': message.get('sender', 'user'),
                'timestamp': self._get_timestamp(),
                'report_format': report_format,
                'report_title': title,
                'report_content': report_content
            }
        except (AgentMessageError, ReportGenerationError) as e:
            # Re-raise specialized exceptions
            logger.error(f"Error in report generation: {str(e)}")
            raise
        except Exception as e:
            # Wrap other exceptions
            logger.error(f"Unexpected error generating report: {str(e)}")
            raise ReportGenerationError(
                self._name,
                f"Failed to generate report: {str(e)}",
                format=message.get('format', 'unknown')
            )
