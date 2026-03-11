import argparse
from dotenv import load_dotenv

# Import commands
from commands.update_tags import register_parser as register_update_tags
from commands.duplicates import register_parser as register_duplicates
from commands.covers import register_parser as register_covers
from commands.identify import register_parser as register_identify
from commands.bitrates import register_parser as register_bitrates
from commands.copies import register_parser as register_copies
from commands.capitalize import register_parser as register_capitalize
from commands.diff import register_parser as register_diff

def main():
    # Load environment variables securely from .env
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="RenameTagMp3 - Audio File Organization CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")
    subparsers.required = True

    # Register subcommand parsers
    register_update_tags(subparsers)
    register_duplicates(subparsers)
    register_covers(subparsers)
    register_identify(subparsers)
    register_bitrates(subparsers)
    register_copies(subparsers)
    register_capitalize(subparsers)
    register_diff(subparsers)

    args = parser.parse_args()
    
    # Run the corresponding command function
    args.func(args)

if __name__ == "__main__":
    main()
