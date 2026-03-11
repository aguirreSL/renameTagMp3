import os
import argparse

def list_files_with_copy(directory):
    files_with_copy = []
    for filename in os.listdir(directory):
        if "2." in filename.lower() or "copy" in filename.lower():
            file_path = os.path.join(directory, filename)
            files_with_copy.append(file_path)
    return files_with_copy

def run_find_copies(args):
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return
        
    files_with_copy = list_files_with_copy(args.dir)
    files_with_copy.sort()
    
    with open(args.out, "w") as file:
        if files_with_copy:
            file.write("Files with 'copy' or '2.' in the title (sorted alphabetically):\n")
            for file_path in files_with_copy:
                file.write(file_path + "\n")
        else:
            file.write("No files with 'copy' or '2.' in the title found.\n")
    
    print(f"Results saved to {args.out}")

def register_parser(subparsers):
    parser = subparsers.add_parser("find-copies", help="Find files with 'copy' or '2.' in their names.")
    parser.add_argument("--dir", required=True, help="Directory to search")
    parser.add_argument("--out", default="files_with_copy.txt", help="Output file name")
    parser.set_defaults(func=run_find_copies)
