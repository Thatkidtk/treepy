# rptree/async_tree.py
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Set
from dataclasses import dataclass
import json
from xml.etree import ElementTree as ET
from datetime import datetime

@dataclass
class AsyncTreeConfig:
    """Configuration for async tree generation"""
    max_depth: int = None
    show_hidden: bool = False
    show_size: bool = False
    show_modified: bool = False
    output_format: str = "text"  # text, json, xml, or html
    exclude_patterns: Set[str] = None
    sort_by: str = "name"  # name, size, or modified

class AsyncDirectoryTree:
    """Asynchronous directory tree generator with multiple output formats"""
    
    def __init__(self, root_path: str, config: AsyncTreeConfig):
        self.root_path = Path(root_path)
        self.config = config
        self.entries = []

    async def generate(self) -> str:
        """Generate the directory tree in the specified format"""
        await self._scan_directory(self.root_path, 0)
        
        if self.config.output_format == "json":
            return self._generate_json()
        elif self.config.output_format == "xml":
            return self._generate_xml()
        elif self.config.output_format == "html":
            return self._generate_html()
        else:
            return self._generate_text()

    async def _scan_directory(self, directory: Path, depth: int) -> dict:
        """Asynchronously scan directory and collect information"""
        if self.config.max_depth is not None and depth >= self.config.max_depth:
            return None

        try:
            entries = []
            async for entry in aiofiles.os.scandir(str(directory)):
                entry_path = Path(entry.path)
                
                # Skip hidden files if not showing them
                if not self.config.show_hidden and entry_path.name.startswith('.'):
                    continue
                
                # Skip excluded patterns
                if self.config.exclude_patterns and any(
                    entry_path.match(pattern) 
                    for pattern in self.config.exclude_patterns
                ):
                    continue

                entry_info = {
                    'name': entry_path.name,
                    'path': str(entry_path),
                    'is_dir': entry_path.is_dir(),
                    'depth': depth
                }

                if self.config.show_size and not entry_path.is_dir():
                    try:
                        stats = await aiofiles.os.stat(entry_path)
                        entry_info['size'] = stats.st_size
                    except OSError:
                        entry_info['size'] = 0

                if self.config.show_modified:
                    try:
                        stats = await aiofiles.os.stat(entry_path)
                        entry_info['modified'] = datetime.fromtimestamp(stats.st_mtime)
                    except OSError:
                        entry_info['modified'] = None

                if entry_path.is_dir():
                    entry_info['children'] = await self._scan_directory(entry_path, depth + 1)

                entries.append(entry_info)

            # Sort entries based on configuration
            entries.sort(key=lambda x: (
                (not x['is_dir'] if self.config.sort_by == 'name' else False),
                x.get(self.config.sort_by, x['name'])
            ))

            return entries

        except PermissionError:
            return None

    def _generate_json(self) -> str:
        """Generate JSON output"""
        return json.dumps(self.entries, default=str, indent=2)

    def _generate_xml(self) -> str:
        """Generate XML output"""
        root = ET.Element("directory-tree")
        
        def add_entry(parent: ET.Element, entry: dict):
            elem = ET.SubElement(parent, "directory" if entry['is_dir'] else "file")
            elem.set("name", entry['name'])
            
            if 'size' in entry:
                elem.set("size", str(entry['size']))
            if 'modified' in entry:
                elem.set("modified", str(entry['modified']))
            
            if entry.get('children'):
                for child in entry['children']:
                    add_entry(elem, child)
        
        for entry in self.entries:
            add_entry(root, entry)
        
        return ET.tostring(root, encoding='unicode', xml_declaration=True)

    def _generate_html(self) -> str:
        """Generate HTML output with collapsible tree structure"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .tree-node { margin-left: 20px; }
                .directory { cursor: pointer; }
                .directory::before { content: "📁 "; }
                .file::before { content: "📄 "; }
                .hidden { display: none; }
            </style>
            <script>
                function toggleNode(element) {
                    const children = element.nextElementSibling;
                    children.classList.toggle('hidden');
                }
            </script>
        </head>
        <body>
            <div class="tree-root">
                {content}
            </div>
        </body>
        </html>
        """

        def format_entry(entry: dict) -> str:
            if entry['is_dir']:
                children = ''.join(format_entry(child) for child in entry.get('children', []))
                return f"""
                    <div>
                        <span class="directory" onclick="toggleNode(this)">{entry['name']}</span>
                        <div class="tree-node">{children}</div>
                    </div>
                """
            else:
                size_info = f" ({entry['size']} bytes)" if 'size' in entry else ""
                modified_info = f" (Modified: {entry['modified']})" if 'modified' in entry else ""
                return f'<div class="file">{entry["name"]}{size_info}{modified_info}</div>'

        content = ''.join(format_entry(entry) for entry in self.entries)
        return html_template.format(content=content)

    def _generate_text(self) -> str:
        """Generate traditional text-based tree output"""
        output = []
        
        def format_entry(entry: dict, prefix: str = "") -> None:
            is_last = entry == self.entries[-1]
            connector = "└──" if is_last else "├──"
            
            # Add size and modification info if available
            extra_info = []
            if 'size' in entry:
                extra_info.append(f"{entry['size']} bytes")
            if 'modified' in entry:
                extra_info.append(f"modified: {entry['modified']}")
            
            extra = f" ({', '.join(extra_info)})" if extra_info else ""
            
            output.append(f"{prefix}{connector} {entry['name']}{extra}")
            
            if entry.get('children'):
                new_prefix = prefix + ("    " if is_last else "│   ")
                for child in entry['children']:
                    format_entry(child, new_prefix)
        
        output.append(self.root_path.name)
        for entry in self.entries:
            format_entry(entry)
        
        return '\n'.join(output)
