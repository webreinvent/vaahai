"""
Tests for the Language Detector Agent.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from vaahai.core.agents.language_detector.language_detector_agent import LanguageDetectorAgent
from vaahai.core.agents.factory import AgentFactory


def test_agent_factory_creates_language_detector():
    """Test that the agent factory can create a language detector agent."""
    agent = AgentFactory.create_agent("language_detector")
    assert isinstance(agent, LanguageDetectorAgent)


def test_detect_from_extension():
    """Test language detection from file extension."""
    agent = LanguageDetectorAgent()
    
    # Test common extensions
    assert agent.detect_from_extension("test.py") == "python"
    assert agent.detect_from_extension("app.js") == "javascript"
    assert agent.detect_from_extension("styles.css") == "css"
    assert agent.detect_from_extension("index.html") == "html"
    assert agent.detect_from_extension("main.cpp") == "c++"
    
    # Test unknown extension
    assert agent.detect_from_extension("file.xyz") == "unknown"


def test_detect_from_content():
    """Test language detection from file content."""
    agent = LanguageDetectorAgent()
    
    # Python content
    python_content = """
    import os
    from pathlib import Path
    
    def main():
        print("Hello, world!")
        
    if __name__ == "__main__":
        main()
    """
    python_scores = agent.detect_from_content(python_content)
    assert "python" in python_scores
    assert python_scores["python"] > 0.5
    
    # JavaScript content
    js_content = """
    const fs = require('fs');
    
    function processFile(path) {
        let content = fs.readFileSync(path, 'utf8');
        return content.split('\\n');
    }
    
    module.exports = { processFile };
    """
    js_scores = agent.detect_from_content(js_content)
    assert "javascript" in js_scores
    assert js_scores["javascript"] > 0.5


def test_detect_features():
    """Test detection of language features."""
    agent = LanguageDetectorAgent()
    
    # Python 3.10 features
    python_310_content = """
    def process_command(command):
        match command:
            case "start":
                return "Starting..."
            case "stop":
                return "Stopping..."
            case _:
                return "Unknown command"
    """
    features = agent.detect_features("python", python_310_content)
    assert "match case" in features or "pattern matching" in features
    
    # JavaScript ES2020 features
    js_es2020_content = """
    const data = {
        user: {
            address: null
        }
    };
    
    const city = data.user?.address?.city ?? "Unknown";
    """
    features = agent.detect_features("javascript", js_es2020_content)
    assert "optional chaining" in features or "nullish coalescing" in features


def test_detect_frameworks():
    """Test detection of frameworks and libraries."""
    agent = LanguageDetectorAgent()
    
    # Django framework
    django_content = """
    from django.db import models
    from django.urls import path
    
    class User(models.Model):
        username = models.CharField(max_length=100)
        email = models.EmailField()
    
    urlpatterns = [
        path('users/', user_list, name='user-list'),
    ]
    """
    frameworks = agent.detect_frameworks("python", django_content)
    assert any(f["name"] == "django" for f in frameworks)
    
    # React framework
    react_content = """
    import React, { useState, useEffect } from 'react';
    
    function App() {
        const [count, setCount] = useState(0);
        
        useEffect(() => {
            document.title = `You clicked ${count} times`;
        }, [count]);
        
        return (
            <div>
                <p>You clicked {count} times</p>
                <button onClick={() => setCount(count + 1)}>
                    Click me
                </button>
            </div>
        );
    }
    
    export default App;
    """
    frameworks = agent.detect_frameworks("javascript", react_content)
    assert any(f["name"] == "react" for f in frameworks)


@patch("vaahai.core.agents.language_detector.language_detector_agent.LanguageDetectorAgent.analyze_with_llm")
async def test_run_with_llm(mock_analyze_with_llm):
    """Test running the agent with LLM analysis."""
    # Mock LLM analysis
    mock_analyze_with_llm.return_value = {
        "language": "python",
        "confidence": 0.95,
        "version": {
            "detected": "3.10+",
            "confidence": 0.8,
            "features": ["pattern matching"]
        },
        "frameworks": [
            {
                "name": "flask",
                "confidence": 0.9,
                "evidence": ["Flask(__name__)", "@app.route"]
            }
        ],
        "additional_languages": [],
        "analysis": "This is a Flask web application written in Python 3.10."
    }
    
    agent = LanguageDetectorAgent()
    result = await agent.run(
        file_paths=["app.py"],
        file_contents=[
            """
            from flask import Flask, request
            
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                return 'Hello, World!'
            
            if __name__ == '__main__':
                app.run(debug=True)
            """
        ],
        use_llm=True
    )
    
    assert result["primary_language"] == "python"
    assert "app.py" in result["file_analyses"]
    assert result["file_analyses"]["app.py"]["language"] == "python"
    assert result["file_analyses"]["app.py"]["frameworks"][0]["name"] == "flask"


@patch("vaahai.core.agents.base.VaahaiAgent._create_autogen_config")
async def test_run_without_llm(mock_create_autogen_config):
    """Test running the agent without LLM analysis."""
    # Mock config to simulate no API key
    mock_create_autogen_config.return_value = {"use_dummy_config": True}
    
    agent = LanguageDetectorAgent()
    result = await agent.run(
        file_paths=["app.py"],
        file_contents=[
            """
            from flask import Flask, request
            
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                return 'Hello, World!'
            
            if __name__ == '__main__':
                app.run(debug=True)
            """
        ],
        use_llm=False
    )
    
    assert result["primary_language"] == "python"
    assert "app.py" in result["file_analyses"]
    assert result["file_analyses"]["app.py"]["language"] == "python"
    assert any(f["name"] == "flask" for f in result["file_analyses"]["app.py"]["frameworks"])


@patch("vaahai.core.agents.language_detector.language_detector_agent.LanguageDetectorAgent.analyze_with_llm")
async def test_multi_file_analysis(mock_analyze_with_llm):
    """Test analysis of multiple files."""
    # Mock LLM analysis for simplicity
    mock_analyze_with_llm.side_effect = [
        {
            "language": "python",
            "confidence": 0.95,
            "version": {"detected": "3.9+", "confidence": 0.8, "features": []},
            "frameworks": [{"name": "flask", "confidence": 0.9, "evidence": []}],
            "additional_languages": [],
            "analysis": "Flask app"
        },
        {
            "language": "javascript",
            "confidence": 0.95,
            "version": {"detected": "ES2020+", "confidence": 0.8, "features": []},
            "frameworks": [{"name": "react", "confidence": 0.9, "evidence": []}],
            "additional_languages": [],
            "analysis": "React component"
        }
    ]
    
    agent = LanguageDetectorAgent()
    result = await agent.run(
        file_paths=["app.py", "component.jsx"],
        file_contents=[
            "from flask import Flask\napp = Flask(__name__)",
            "import React from 'react'\nfunction App() { return <div>Hello</div> }"
        ],
        use_llm=True
    )
    
    assert len(result["file_analyses"]) == 2
    assert result["language_distribution"] == {"python": 1, "javascript": 1}
    assert result["file_analyses"]["app.py"]["language"] == "python"
    assert result["file_analyses"]["component.jsx"]["language"] == "javascript"
