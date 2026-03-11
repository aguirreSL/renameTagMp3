import os
import argparse

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.m4a'):
            name, ext = os.path.splitext(filename)
            new_name = ' '.join(word.capitalize() for word in name.split())
            new_filename = f"{new_name}{ext}"
            
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            
            os.rename(old_file, new_file)
            print(f"Renamed: {filename} -> {new_filename}")

def run_capitalize(args):
    """Capitalize words in .m4a filenames."""
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return
    process_directory(args.dir)

def register_parser(subparsers):
    parser = subparsers.add_parser("capitalize", help="Capitalize words in .m4a filenames.")
    parser.add_argument("--dir", required=True, help="Directory containing .m4a files")
    parser.set_defaults(func=run_capitalize)
