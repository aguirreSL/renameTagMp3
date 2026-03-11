import os
import argparse
import hashlib

def calculate_file_hash(file_path, hash_algorithm="md5", block_size=65536):
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hash_func.update(block)
    return hash_func.hexdigest()

def run_find_duplicates(args):
    """Find duplicated files using MD5 hashing."""
    if not os.path.isdir(args.dir):
        print(f"Directory not found: {args.dir}")
        return

    hashes = {}
    duplicates = {}

    for root, _, files in os.walk(args.dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)

            if file_hash in hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [hashes[file_hash]]
                duplicates[file_hash].append(file_path)
            else:
                hashes[file_hash] = file_path

    with open(args.out, "w") as f:
        for file_hash, file_paths in duplicates.items():
            f.write(f"Duplicate files (Hash: {file_hash}):\n")
            for path in file_paths:
                f.write(f"{path}\n")
            f.write("\n")
            
    print(f"Duplicates list saved to {args.out}")

def register_parser(subparsers):
    parser = subparsers.add_parser("find-duplicates", help="Find duplicate files across a directory.")
    parser.add_argument("--dir", required=True, help="Directory to search for duplicates")
    parser.add_argument("--out", default="duplicates_list.txt", help="Output file for list of duplicates")
    parser.set_defaults(func=run_find_duplicates)
