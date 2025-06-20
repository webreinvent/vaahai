#!/usr/bin/env python
"""
Example demonstrating the LLMLanguageFrameworkCMSDetectionAgent.

This script shows how to use the LLMLanguageFrameworkCMSDetectionAgent to detect
the programming language, framework, and CMS from code content.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vaahai.review.agents.detection import LLMLanguageFrameworkCMSDetectionAgent
from vaahai.config.manager import ConfigManager
from vaahai.utils.llm_client import get_llm_client

# Create a rich console for formatted output
console = Console()

def format_confidence(confidence):
    """Format confidence score with color based on value."""
    if confidence >= 0.8:
        return f"[green]{confidence:.2f}[/green]"
    elif confidence >= 0.5:
        return f"[yellow]{confidence:.2f}[/yellow]"
    else:
        return f"[red]{confidence:.2f}[/red]"

def main():
    """Run the example."""
    # Check if configuration exists
    config_manager = ConfigManager()
    
    # Check if default LLM provider is configured
    default_provider = config_manager.get("llm.default_provider")
    if not default_provider:
        console.print(
            Panel(
                "[bold red]Default LLM provider not configured![/bold red]\n"
                "Please run [bold]vaahai config init[/bold] first to set up your LLM configuration.",
                title="Error",
                border_style="red",
            )
        )
        return

    # Create the detection agent
    agent = LLMLanguageFrameworkCMSDetectionAgent({"name": "ExampleDetection"})
    
    # Example code snippets
    examples = [
        {
            "name": "Python/Django",
            "code": """
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
"""
        },
        {
            "name": "JavaScript/React",
            "code": """
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserList() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    axios.get('/api/users')
      .then(response => setUsers(response.data))
      .catch(error => console.error(error));
  }, []);
  
  return (
    <div className="user-list">
      <h2>User List</h2>
      <ul>
        {users.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;
"""
        },
        {
            "name": "PHP/WordPress",
            "code": """
<?php
/**
 * Custom WordPress widget
 */
class My_Custom_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'my_custom_widget',
            'My Custom Widget',
            array('description' => 'A custom WordPress widget')
        );
    }
    
    public function widget($args, $instance) {
        echo $args['before_widget'];
        echo $args['before_title'] . $instance['title'] . $args['after_title'];
        echo '<div class="widget-content">' . $instance['content'] . '</div>';
        echo $args['after_widget'];
    }
    
    public function form($instance) {
        $title = isset($instance['title']) ? $instance['title'] : 'Default Title';
        $content = isset($instance['content']) ? $instance['content'] : '';
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>">Title:</label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" 
                   name="<?php echo $this->get_field_name('title'); ?>" type="text" 
                   value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label for="<?php echo $this->get_field_id('content'); ?>">Content:</label>
            <textarea class="widefat" id="<?php echo $this->get_field_id('content'); ?>" 
                     name="<?php echo $this->get_field_name('content'); ?>"><?php echo esc_textarea($content); ?></textarea>
        </p>
        <?php
    }
    
    public function update($new_instance, $old_instance) {
        $instance = array();
        $instance['title'] = (!empty($new_instance['title'])) ? strip_tags($new_instance['title']) : '';
        $instance['content'] = (!empty($new_instance['content'])) ? $new_instance['content'] : '';
        return $instance;
    }
}

function register_my_custom_widget() {
    register_widget('My_Custom_Widget');
}
add_action('widgets_init', 'register_my_custom_widget');
"""
        }
    ]
    
    # Process each example
    for example in examples:
        console.print(f"\n[bold]Processing example: {example['name']}[/bold]")
        
        with console.status(f"Detecting language, framework, and CMS for {example['name']}..."):
            result = agent.run(example['code'])
        
        # Create a table to display the results
        table = Table(title=f"Detection Results for {example['name']}")
        table.add_column("Type", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Confidence", justify="right")
        
        # Add rows for language, framework, and CMS
        language = result["primary_language"]["name"] or "Unknown"
        language_confidence = result["primary_language"]["confidence"] or 0.0
        table.add_row("Language", language, format_confidence(language_confidence))
        
        framework = result["primary_framework"]["name"] or "None detected"
        framework_confidence = result["primary_framework"]["confidence"] or 0.0
        table.add_row("Framework", framework, format_confidence(framework_confidence))
        
        cms = result["primary_cms"]["name"] or "None detected"
        cms_confidence = result["primary_cms"]["confidence"] or 0.0
        table.add_row("CMS", cms, format_confidence(cms_confidence))
        
        console.print(table)

if __name__ == "__main__":
    main()
