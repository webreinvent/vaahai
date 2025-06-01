"""
Tests for the code scanner module.
"""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

from vaahai.core.scanner import code_scanner, CodeScanner, FileInfo
from vaahai.core.scanner.filters import (
    LanguageFilter, SizeFilter, ExtensionFilter, PatternFilter, 
    RegexFilter, ContentFilter, CompositeFilter
)


class TestCodeScanner:
    """Test the CodeScanner class."""
    
    @pytest.fixture
    def setup_test_directory(self):
        """Set up a temporary directory with test files."""
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Create test files
            files = {
                "test.py": "def hello():\n    print('Hello, world!')",
                "test.js": "function hello() {\n    console.log('Hello, world!');\n}",
                "test.txt": "This is a text file.",
                "large.bin": "x" * (1024 * 1024 + 1),  # Just over 1MB
                "nested/test.py": "def nested():\n    print('Nested!')",
                "nested/deep/test.go": "package main\n\nfunc main() {\n    println(\"Hello, Go!\")\n}",
                ".hidden/test.py": "# Hidden file",
                "node_modules/test.js": "// Should be excluded"
            }
            
            # Create the files
            for file_path, content in files.items():
                full_path = os.path.join(temp_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)
            
            yield temp_dir
        finally:
            # Clean up
            shutil.rmtree(temp_dir)
    
    def test_singleton_pattern(self):
        """Test that CodeScanner implements the singleton pattern."""
        scanner1 = CodeScanner()
        scanner2 = CodeScanner()
        assert scanner1 is scanner2
        assert code_scanner is scanner1
    
    def test_scan_file(self, setup_test_directory):
        """Test scanning a single file."""
        temp_dir = setup_test_directory
        test_py = os.path.join(temp_dir, "test.py")
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Scan a single file
        results = code_scanner.scan_path(test_py)
        
        assert len(results) == 1
        assert results[0].path == os.path.abspath(test_py)
        assert results[0].language == "python"
        assert results[0].size > 0
    
    def test_scan_directory(self, setup_test_directory):
        """Test scanning a directory."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should find test.py, test.js, nested/test.py, nested/deep/test.go
        # But not node_modules/test.js (excluded dir) or large.bin (too large)
        assert len(results) == 4
        
        # Check that we found the expected files
        paths = [os.path.relpath(f.path, temp_dir) for f in results]
        assert "test.py" in paths
        assert "test.js" in paths
        assert os.path.join("nested", "test.py") in paths
        assert os.path.join("nested", "deep", "test.go") in paths
        
        # Check that excluded files are not included
        assert os.path.join("node_modules", "test.js") not in paths
        assert "large.bin" not in paths
    
    def test_file_filters(self, setup_test_directory):
        """Test file filters."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Add a language filter to only include Python files
        code_scanner.add_filter(LanguageFilter(["python"]))
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should only find Python files
        assert len(results) == 2
        languages = [f.language for f in results]
        assert all(lang == "python" for lang in languages)
        
        # Reset and try a different filter
        code_scanner.reset()
        code_scanner.add_filter(ExtensionFilter([".js", ".go"]))
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should only find JS and Go files
        assert len(results) == 2
        extensions = [f.extension for f in results]
        assert all(ext in [".js", ".go"] for ext in extensions)
    
    def test_content_loading(self, setup_test_directory):
        """Test loading file content."""
        temp_dir = setup_test_directory
        test_py = os.path.join(temp_dir, "test.py")
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Scan and load content
        results = code_scanner.scan_and_load_content([test_py])
        
        assert len(results) == 1
        assert "def hello()" in results[0].content
    
    def test_content_filter(self, setup_test_directory):
        """Test filtering by content."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Add a content filter to find files containing "print"
        code_scanner.add_filter(ContentFilter("print"))
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should find files containing "print"
        assert len(results) == 2  # test.py and nested/test.py
        
        # Check that all files contain "print"
        for file_info in results:
            assert "print" in file_info.load_content()
    
    def test_composite_filter(self, setup_test_directory):
        """Test composite filters."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Create a composite filter: Python files containing "print"
        language_filter = LanguageFilter(["python"])
        content_filter = ContentFilter("print")
        composite = CompositeFilter([language_filter, content_filter])
        
        code_scanner.add_filter(composite)
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should find Python files containing "print"
        assert len(results) == 2  # test.py and nested/test.py
        
        # Check that all files are Python and contain "print"
        for file_info in results:
            assert file_info.language == "python"
            assert "print" in file_info.load_content()
    
    def test_glob_pattern(self, setup_test_directory):
        """Test scanning with glob patterns."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Scan with a glob pattern
        pattern = os.path.join(temp_dir, "**", "*.py")
        results = code_scanner.scan_path(pattern)
        
        # Should find all Python files
        assert len(results) == 2  # test.py and nested/test.py
        
        # Check that all files are Python
        for file_info in results:
            assert file_info.extension == ".py"
    
    def test_exclude_patterns(self, setup_test_directory):
        """Test excluding files with patterns."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Add an exclude pattern
        nested_pattern = os.path.join(temp_dir, "nested", "*")
        code_scanner.add_exclude_pattern(nested_pattern)
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should not find files in the nested directory
        paths = [f.path for f in results]
        assert not any("nested" in p for p in paths)
    
    def test_include_patterns(self, setup_test_directory):
        """Test including files with patterns."""
        temp_dir = setup_test_directory
        
        # Reset scanner to default settings
        code_scanner.reset()
        
        # Set include patterns to only include .txt files
        txt_pattern = os.path.join(temp_dir, "*.txt")
        code_scanner.set_include_patterns([txt_pattern])
        
        # Scan the directory
        results = code_scanner.scan_path(temp_dir)
        
        # Should only find .txt files
        assert len(results) == 1
        assert results[0].extension == ".txt"
