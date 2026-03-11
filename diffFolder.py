import os

def list_files(directory):
    """List all files in a directory recursively."""
    file_set = set()
    for root, _, files in os.walk(directory):
        for file in files:
            # Store the relative path to the file
            rel_path = os.path.relpath(os.path.join(root, file), directory)
            file_set.add(rel_path)
    return file_set

def compare_directories(dir1, dir2, output_file):
    """Compare two directories and list files unique to each."""
    files_dir1 = list_files(dir1)
    files_dir2 = list_files(dir2)

    # Files only in dir1
    only_in_dir1 = sorted(files_dir1 - files_dir2)  # Sort alphabetically
    # Files only in dir2
    only_in_dir2 = sorted(files_dir2 - files_dir1)  # Sort alphabetically

    # Write results to the output file
    with open(output_file, "w") as f:
        f.write(f"Files only in {dir1}\n")
        for file in only_in_dir1:
            f.write(f"{file}\n")

        f.write(f"\nFiles only in {dir2}\n")
        for file in only_in_dir2:
            f.write(f"{file}\n")

    print(f"Comparison results saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compare two directories and output unique files.")
    parser.add_argument("--dir1", required=True, help="First directory")
    parser.add_argument("--dir2", required=True, help="Second directory")
    parser.add_argument("--out", default="comparison_results.txt", help="Output file")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir1) and os.path.isdir(args.dir2):
        compare_directories(args.dir1, args.dir2, args.out)
    else:
        print("One or both input directories are invalid.")