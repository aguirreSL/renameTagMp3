import os
import argparse
from core.files import walk_audio_files
from core.tags import sync_tags_with_filename

def run_update_tags(args):
    """Command to parse filenames and sync tags across a directory."""
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return

    for file_path in walk_audio_files(args.dir):
        print(f"\nProcessing: {os.path.basename(file_path)}")
        changed, message = sync_tags_with_filename(file_path)
        if changed:
            print(f"Updated: {message}")
        else:
            print(f"No changes needed: {message}")

def register_parser(subparsers):
    parser = subparsers.add_parser("update-tags", help="Update metadata tags by parsing artist and title from filenames.")
    parser.add_argument("--dir", required=True, help="Directory containing audio files")
    parser.set_defaults(func=run_update_tags)
