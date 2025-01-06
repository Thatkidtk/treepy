# RPTree - Directory Tree Generator

A Python command-line tool to generate visually appealing directory tree diagrams.

## Features

- Generate directory tree diagrams with Unicode box-drawing characters or ASCII
- Customize output depth, hidden files visibility, and file size display
- Save output to file or display in console
- Cross-platform compatibility using `pathlib`
- Clear error handling and user feedback

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rptree.git
cd rptree
```

2. Install the package:
```bash
pip install -e .
```

## Usage

Basic usage:
```bash
python -m rptree /path/to/directory
```

Options:
- `-d, --max-depth`: Maximum depth of the directory tree
- `--hidden`: Show hidden files and directories
- `--size`: Show file sizes
- `--ascii`: Use ASCII characters instead of Unicode box drawings
- `-o, --output`: Save output to a file

Examples:
```bash
# Generate tree with file sizes
python -m rptree /path/to/directory --size

# Limit depth to 2 levels
python -m rptree /path/to/directory -d 2

# Save output to file
python -m rptree /path/to/directory -o tree.txt
```

## Development

To set up the development environment:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.# treepy
