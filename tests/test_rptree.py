# tests/test_rptree.py
import pytest
from pathlib import Path
import tempfile
import os
import shutil
from rptree.rptree import DirectoryTree, TreeConfig

@pytest.fixture
def temp_directory():
    """Create a temporary directory with a known structure for testing"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a test directory structure
        root = Path(tmp_dir)
        
        # Create directories
        (root / "dir1").mkdir()
        (root / "dir1" / "subdir1").mkdir()
        (root / "dir2").mkdir()
        
        # Create files
        (root / "file1.txt").write_text("content1")
        (root / "dir1" / "file2.txt").write_text("content2")
        (root / "dir1" / "subdir1" / "file3.txt").write_text("content3")
        (root / ".hidden_file").write_text("hidden")
        (root / "dir2" / "large_file").write_bytes(b"0" * 1024 * 1024)  # 1MB file
        
        yield tmp_dir

def test_basic_tree_generation(temp_directory):
    """Test basic tree generation without any special options"""
    config = TreeConfig()
    tree = DirectoryTree(temp_directory, config)
    result = tree.generate()
    
    # Verify basic structure
    assert len(result) > 0
    assert Path(temp_directory).name in result[0]
    assert any("dir1" in line for line in result)
    assert any("dir2" in line for line in result)
    assert any("file1.txt" in line for line in result)

def test_max_depth_limit(temp_directory):
    """Test that max_depth properly limits directory traversal"""
    config = TreeConfig(max_depth=1)
    tree = DirectoryTree(temp_directory, config)
    result = tree.generate()
    
    # Should show root and immediate children, but not deeper contents
    assert not any("file3.txt" in line for line in result)
    assert any("dir1" in line for line in result)

def test_hidden_files(temp_directory):
    """Test showing/hiding hidden files"""
    # Test without showing hidden files
    config = TreeConfig(show_hidden=False)
    tree = DirectoryTree(temp_directory, config)
    result = tree.generate()
    assert not any(".hidden_file" in line for line in result)
    
    # Test with showing hidden files
    config = TreeConfig(show_hidden=True)
    tree = DirectoryTree(temp_directory, config)
    result = tree.generate()
    assert any(".hidden_file" in line for line in result)

def test_file_size_display(temp_directory):
    """Test file size display functionality"""
    config = TreeConfig(show_size=True)
    tree = DirectoryTree(temp_directory, config)
    result = tree.generate()
    
    # Check if file sizes are shown
    large_file_line = next(line for line in result if "large_file" in line)
    assert "1.0MB" in large_file_line

def test_ascii_output(temp_directory):
    """Test ASCII output mode"""
    config = TreeConfig(use_ascii=True)
    tree = DirectoryTree(temp_directory, config)
    result = tree.generate()
    
    # Verify ASCII characters are used
    assert any("|--" in line for line in result)
    assert not any("├──" in line for line in result)

# tests/test_cli.py
import pytest
from rptree.cli import parse_args
import sys
from unittest.mock import patch

def test_cli_arguments():
    """Test command-line argument parsing"""
    test_args = ['script_name', '/test/path', '--max-depth', '2', '--hidden', '--size']
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args.root_path == '/test/path'
        assert args.max_depth == 2
        assert args.hidden is True
        assert args.size is True
        assert args.ascii is False

def test_cli_output_file(temp_directory):
    """Test writing output to a file"""
    from rptree.cli import main
    output_file = Path(temp_directory) / "output.txt"
    
    test_args = ['script_name', temp_directory, '-o', str(output_file)]
    with patch.object(sys, 'argv', test_args):
        main()
        
    assert output_file.exists()
    content = output_file.read_text()
    assert len(content.splitlines()) > 0
