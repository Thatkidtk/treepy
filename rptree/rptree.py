# rptree/rptree.py
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import sys

@dataclass
class TreeConfig:
    """Configuration for tree generation"""
    max_depth: Optional[int] = None
    show_hidden: bool = False
    show_size: bool = False
    use_ascii: bool = False
    output_file: Optional[str] = None

class DirectoryTree:
    """Generate a directory tree diagram"""
    
    # Box drawing characters for the tree structure
    PIPE = "│" 
    ELBOW = "└──"
    TEE = "├──"
    PIPE_PREFIX = "│   "
    SPACE_PREFIX = "    "

    def __init__(self, root_path: str, config: TreeConfig):
        self.root_path = Path(root_path)
        self.config = config
        self.tree_output = []
        
        # Use ASCII characters if specified
        if self.config.use_ascii:
            self.PIPE = "|"
            self.ELBOW = "`--"
            self.TEE = "|--"
            self.PIPE_PREFIX = "|   "

    def generate(self) -> List[str]:
        """Generate the directory tree diagram"""
        self.tree_output = []
        self._add_root(self.root_path)
        self._walk_directory(self.root_path, "", 0)
        return self.tree_output

    def _add_root(self, path: Path) -> None:
        """Add the root directory to the tree output"""
        self.tree_output.append(f"{path.name}{Path.sep}")

    def _walk_directory(self, directory: Path, prefix: str, depth: int) -> None:
        """Recursively walk through directories and add items to the tree output"""
        if self.config.max_depth is not None and depth >= self.config.max_depth:
            return

        # Get and sort directory contents
        entries = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        entries_count = len(entries)

        for index, entry in enumerate(entries):
            if not self.config.show_hidden and entry.name.startswith('.'):
                continue

            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            next_prefix = (self.SPACE_PREFIX if index == entries_count - 1 else self.PIPE_PREFIX)

            entry_name = entry.name
            if entry.is_dir():
                entry_name = f"{entry_name}{Path.sep}"
            elif self.config.show_size:
                try:
                    size = entry.stat().st_size
                    entry_name = f"{entry_name} ({self._format_size(size)})"
                except OSError:
                    entry_name = f"{entry_name} (error)"

            self.tree_output.append(f"{prefix}{connector} {entry_name}")

            if entry.is_dir():
                self._walk_directory(entry, f"{prefix}{next_prefix}", depth + 1)

    @staticmethod
    def _format_size(size: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}PB"