"""
Review steps runner.

This module provides utilities for running multiple review steps on code.
"""

import logging
import os
from typing import Any, Dict, List, Optional, Set, Union

from vaahai.review.steps.base import ReviewStep, ReviewStepCategory, ReviewStepSeverity
from vaahai.review.steps.registry import ReviewStepRegistry

# Setup logging
logger = logging.getLogger(__name__)


class ReviewRunner:
    """
    Runner for executing multiple review steps on code.
    
    This class provides utilities for running multiple review steps on code
    and aggregating the results.
    """
    
    def __init__(
        self,
        steps: Optional[List[Union[str, ReviewStep]]] = None,
        categories: Optional[List[ReviewStepCategory]] = None,
        severities: Optional[List[ReviewStepSeverity]] = None,
        tags: Optional[List[str]] = None,
        enabled_only: bool = True,
    ):
        """
        Initialize the review runner.
        
        Args:
            steps: Optional list of review step IDs or instances to run.
                  If not provided, all steps matching the other criteria will be used.
            categories: Optional list of categories to filter steps by.
            severities: Optional list of severities to filter steps by.
            tags: Optional list of tags to filter steps by.
            enabled_only: If True, only run enabled steps.
        """
        self.step_instances = []
        
        # If specific steps are provided, use those
        if steps:
            for step in steps:
                if isinstance(step, ReviewStep):
                    self.step_instances.append(step)
                elif isinstance(step, str):
                    step_instance = ReviewStepRegistry.create_step_instance(step)
                    if step_instance:
                        self.step_instances.append(step_instance)
                    else:
                        logger.warning(f"Review step '{step}' not found or could not be created")
        else:
            # Otherwise, filter steps based on criteria
            filtered_steps = ReviewStepRegistry.filter_steps(
                category=categories,
                severity=severities,
                tags=tags,
                enabled_only=enabled_only,
            )
            
            # Create instances of the filtered steps
            for step_id, step_class in filtered_steps.items():
                step_instance = ReviewStepRegistry.create_step_instance(step_id)
                if step_instance:
                    self.step_instances.append(step_instance)
    
    def run_on_content(
        self, content: str, file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run all review steps on the provided content.
        
        Args:
            content: The code content to review.
            file_path: Optional path to the file being reviewed.
        
        Returns:
            Dictionary containing the aggregated results of all review steps.
        """
        if content is None or not content.strip():
            return {
                "status": "error",
                "message": "No content provided for review",
                "results": [],
                "total_issues": 0,
            }
        
        context = {
            "content": content,
            "file_path": file_path,
        }
        
        results = []
        total_issues = 0
        
        for step in self.step_instances:
            try:
                step_result = step.execute(context)
                step_result["step_id"] = step.id
                step_result["step_name"] = step.name
                step_result["step_category"] = step.category.name
                step_result["step_severity"] = step.severity.name
                
                results.append(step_result)
                total_issues += len(step_result.get("issues", []))
            except Exception as e:
                logger.error(f"Error running review step '{step.id}': {e}")
                results.append({
                    "step_id": step.id,
                    "step_name": step.name,
                    "step_category": step.category.name if hasattr(step, "category") else "unknown",
                    "step_severity": step.severity.name if hasattr(step, "severity") else "unknown",
                    "status": "error",
                    "message": f"Error running review step: {str(e)}",
                    "issues": [],
                })
        
        return {
            "status": "success",
            "message": f"Ran {len(results)} review steps, found {total_issues} issues",
            "results": results,
            "total_issues": total_issues,
        }
    
    def run_on_file(self, file_path: str) -> Dict[str, Any]:
        """
        Run all review steps on the specified file.
        
        Args:
            file_path: Path to the file to review.
        
        Returns:
            Dictionary containing the aggregated results of all review steps.
        """
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return {
                "status": "error",
                "message": f"File not found: {file_path}",
                "results": [],
                "total_issues": 0,
            }
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return self.run_on_content(content, file_path)
        except Exception as e:
            logger.error(f"Error reading file '{file_path}': {e}")
            return {
                "status": "error",
                "message": f"Error reading file: {str(e)}",
                "results": [],
                "total_issues": 0,
            }
    
    def run_on_directory(
        self,
        directory_path: str,
        file_extensions: Optional[List[str]] = None,
        recursive: bool = True,
        exclude_dirs: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Run all review steps on files in the specified directory.
        
        Args:
            directory_path: Path to the directory to review.
            file_extensions: Optional list of file extensions to include (e.g., ['.py', '.js']).
                           If not provided, all files will be reviewed.
            recursive: If True, review files in subdirectories as well.
            exclude_dirs: Optional list of directory names to exclude.
        
        Returns:
            Dictionary containing the aggregated results of all review steps.
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return {
                "status": "error",
                "message": f"Directory not found: {directory_path}",
                "results": [],
                "total_issues": 0,
            }
        
        exclude_dirs = exclude_dirs or [".git", "__pycache__", "venv", ".venv", "node_modules"]
        file_results = []
        total_issues = 0
        
        for root, dirs, files in os.walk(directory_path):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Process files in the current directory
            for file in files:
                # Skip files with unwanted extensions
                if file_extensions and not any(file.endswith(ext) for ext in file_extensions):
                    continue
                
                file_path = os.path.join(root, file)
                file_result = self.run_on_file(file_path)
                
                if file_result["status"] == "success":
                    file_results.append({
                        "file_path": file_path,
                        "results": file_result["results"],
                        "total_issues": file_result["total_issues"],
                    })
                    total_issues += file_result["total_issues"]
            
            # If not recursive, break after the first iteration
            if not recursive:
                break
        
        return {
            "status": "success",
            "message": f"Reviewed {len(file_results)} files, found {total_issues} issues",
            "file_results": file_results,
            "total_issues": total_issues,
        }
