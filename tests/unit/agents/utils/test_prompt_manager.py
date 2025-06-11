"""
Unit tests for the PromptManager class.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from vaahai.agents.utils.prompt_manager import PromptManager


class TestPromptManager(unittest.TestCase):
    """Tests for the PromptManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for test templates
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        
        # Create mock directory structure
        self.shared_dir = self.base_dir / "agents" / "prompts"
        self.core_dir = self.base_dir / "agents" / "core" / "test_agent" / "prompts"
        self.app_dir = self.base_dir / "agents" / "applications" / "test_agent" / "prompts"
        
        # Create directories
        os.makedirs(self.shared_dir, exist_ok=True)
        os.makedirs(self.core_dir, exist_ok=True)
        os.makedirs(self.app_dir, exist_ok=True)
        
        # Create test templates
        with open(self.shared_dir / "shared.md", "w") as f:
            f.write("# Shared Template\nHello {{ name }}!")
            
        with open(self.core_dir / "core.md", "w") as f:
            f.write("# Core Template\nWelcome {{ name }}!")
            
        with open(self.app_dir / "app.md", "w") as f:
            f.write("# App Template\nGreetings {{ name }}!")
            
        # Create a template in multiple locations to test precedence
        with open(self.shared_dir / "common.md", "w") as f:
            f.write("# Shared Common\nShared {{ name }}!")
            
        with open(self.core_dir / "common.md", "w") as f:
            f.write("# Core Common\nCore {{ name }}!")
    
    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_get_prompt_directories(self, mock_path):
        """Test that prompt directories are found correctly."""
        # Mock the base directory to use our temporary directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Test with a core agent
        manager = PromptManager("test_agent")
        dirs = manager._get_prompt_directories()
        
        # Should include both core and shared directories
        self.assertEqual(len(dirs), 3)
        self.assertIn(str(self.core_dir), dirs)
        self.assertIn(str(self.app_dir), dirs)
        self.assertIn(str(self.shared_dir), dirs)
        
        # Core directory should come first (higher precedence)
        self.assertEqual(dirs[0], str(self.core_dir))
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_render_prompt(self, mock_path):
        """Test rendering a prompt template."""
        # Mock the base directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Create manager and render a template
        manager = PromptManager("test_agent")
        result = manager.render_prompt("shared", {"name": "World"})
        
        self.assertEqual(result, "# Shared Template\nHello World!")
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_template_precedence(self, mock_path):
        """Test that template precedence works correctly."""
        # Mock the base directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Create manager and render the common template
        # Should use the core version due to precedence
        manager = PromptManager("test_agent")
        result = manager.render_prompt("common", {"name": "World"})
        
        self.assertEqual(result, "# Core Common\nCore World!")
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_template_not_found(self, mock_path):
        """Test error handling for missing templates."""
        # Mock the base directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Create manager and try to render a non-existent template
        manager = PromptManager("test_agent")
        
        with self.assertRaises(ValueError) as context:
            manager.render_prompt("nonexistent", {"name": "World"})
            
        self.assertIn("Template not found", str(context.exception))
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_list_templates(self, mock_path):
        """Test listing available templates."""
        # Mock the base directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Create manager and list templates
        manager = PromptManager("test_agent")
        templates = manager.list_templates()
        
        # Should include all templates
        self.assertIn("shared", templates)
        self.assertIn("core", templates)
        self.assertIn("common", templates)
        self.assertIn("app", templates)
        
        # Should be 4 unique templates (common appears twice but should be counted once)
        self.assertEqual(len(set(templates)), 4)
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_get_template_path(self, mock_path):
        """Test getting the path to a template file."""
        # Mock the base directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Create manager and get template path
        manager = PromptManager("test_agent")
        path = manager.get_template_path("shared")
        
        # Should return the path to the shared template
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(os.path.basename(path), "shared.md")
    
    @mock.patch("vaahai.agents.utils.prompt_manager.Path")
    def test_nonexistent_agent_type(self, mock_path):
        """Test behavior with a non-existent agent type."""
        # Mock the base directory
        mock_path.return_value.parent.parent.parent = self.base_dir
        
        # Create manager for a non-existent agent type
        manager = PromptManager("nonexistent_agent")
        dirs = manager._get_prompt_directories()
        
        # Should only include the shared directory
        self.assertEqual(len(dirs), 1)
        self.assertEqual(dirs[0], str(self.shared_dir))
        
        # Should still be able to render shared templates
        result = manager.render_prompt("shared", {"name": "World"})
        self.assertEqual(result, "# Shared Template\nHello World!")


if __name__ == "__main__":
    unittest.main()
