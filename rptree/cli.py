# rptree/cli.py
import argparse
from pathlib import Path
from .rptree import DirectoryTree, TreeConfig
import sys

def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate a directory tree diagram",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "root_path",
        metavar="ROOT_PATH",
        help="Root directory to start generating the tree"
    )
    
    parser.add_argument(
        "-d", "--max-depth",
        type=int,
        help="Maximum depth of the directory tree",
        default=None
    )
    
    parser.add_argument(
        "--hidden",
        action="store_true",
        help="Show hidden files and directories"
    )
    
    parser.add_argument(
        "--size",
        action="store_true",
        help="Show file sizes"
    )
    
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Use ASCII characters instead of Unicode box drawings"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (defaults to stdout)",
        default=None
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the command-line interface"""
    args = parse_args()
    
    # Validate root path
    root_path = Path(args.root_path)
    if not root_path.exists():
        print(f"Error: Directory '{root_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    if not root_path.is_dir():
        print(f"Error: '{root_path}' is not a directory", file=sys.stderr)
        sys.exit(1)
    
    # Create configuration
    config = TreeConfig(
        max_depth=args.max_depth,
        show_hidden=args.hidden,
        show_size=args.size,
        use_ascii=args.ascii,
        output_file=args.output
    )
    
    try:
        # Generate tree
        tree = DirectoryTree(str(root_path), config)
        output = "\n".join(tree.generate())
        
        # Handle output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output + "\n")
        else:
            print(output)
            
    except PermissionError as e:
        print(f"Error: Permission denied accessing '{e.filename}'", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()