"""
Model tracking system for review steps.

This module provides utilities for tracking which LLM model is used for each review step.
"""

import logging
from typing import Dict, List, Optional, Any

# Setup logging
logger = logging.getLogger(__name__)


class ModelTracker:
    """
    Tracks which LLM model is used for each review step.
    
    This class provides utilities for recording and retrieving information about
    which LLM model is used for each step of the review process.
    """
    
    def __init__(self):
        """Initialize the model tracker."""
        self.step_models = {}
        self.model_usage_counts = {}
    
    def record_model_usage(self, step_id: str, model_info: Dict[str, Any]) -> None:
        """
        Record which model was used for a specific review step.
        
        Args:
            step_id: ID of the review step
            model_info: Dictionary containing model information
                        (provider, model_name, temperature, etc.)
        """
        self.step_models[step_id] = model_info
        
        # Update usage counts
        model_key = f"{model_info.get('provider', 'unknown')}/{model_info.get('model_name', 'unknown')}"
        self.model_usage_counts[model_key] = self.model_usage_counts.get(model_key, 0) + 1
        
        logger.debug(f"Recorded model usage for step {step_id}: {model_info}")
    
    def get_model_for_step(self, step_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the model information for a specific review step.
        
        Args:
            step_id: ID of the review step
            
        Returns:
            Dictionary containing model information or None if not recorded
        """
        return self.step_models.get(step_id)
    
    def get_all_model_usage(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all recorded model usage information.
        
        Returns:
            Dictionary mapping step IDs to model information
        """
        return self.step_models
    
    def get_model_usage_summary(self) -> Dict[str, int]:
        """
        Get a summary of model usage counts.
        
        Returns:
            Dictionary mapping model names to usage counts
        """
        return self.model_usage_counts
    
    def clear(self) -> None:
        """Clear all recorded model usage information."""
        self.step_models = {}
        self.model_usage_counts = {}


# Create a singleton instance of the model tracker
model_tracker = ModelTracker()
