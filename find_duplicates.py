import os
import hashlib

def calculate_file_hash(file_path, hash_algorithm="md5", block_size=65536):
    """Calculate the hash of a file."""
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hash_func.update(block)
    return hash_func.hexdigest()

def find_duplicates(directory):
    """Find duplicated files in a directory."""
    hashes = {}
    duplicates = {}

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_file_hash(file_path)

            # Check if the hash already exists
            if file_hash in hashes:
                if file_hash not in duplicates:
                    duplicates[file_hash] = [hashes[file_hash]]  # Add the first file with this hash
                duplicates[file_hash].append(file_path)  # Add the duplicate file
            else:
                hashes[file_hash] = file_path  # Store the file path with its hash

    return duplicates

def save_duplicates_to_file(duplicates, output_file):
    """Save the list of duplicates to a file."""
    with open(output_file, "w") as f:
        for file_hash, file_paths in duplicates.items():
            f.write(f"Duplicate files (Hash: {file_hash}):\n")
            for path in file_paths:
                f.write(f"{path}\n")
            f.write("\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find duplicated files using MD5 hashing.")
    parser.add_argument("--dir", required=True, help="Directory to search for duplicates")
    parser.add_argument("--out", default="duplicates_list.txt", help="Output list file")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        # Find duplicates
        duplicates = find_duplicates(args.dir)
        
        # Save duplicates to a file
        save_duplicates_to_file(duplicates, args.out)
        
        print(f"Duplicates list saved to {args.out}")
    else:
        print(f"Directory not found: {args.dir}")