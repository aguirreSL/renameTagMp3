import os
import argparse

def list_files(directory):
    file_set = set()
    for root, _, files in os.walk(directory):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), directory)
            file_set.add(rel_path)
    return file_set

def compare_directories(dir1, dir2, output_file):
    files_dir1 = list_files(dir1)
    files_dir2 = list_files(dir2)

    only_in_dir1 = sorted(files_dir1 - files_dir2)
    only_in_dir2 = sorted(files_dir2 - files_dir1)

    with open(output_file, "w") as f:
        f.write(f"Files only in {dir1}\n")
        for file in only_in_dir1:
            f.write(f"{file}\n")
        f.write(f"\nFiles only in {dir2}\n")
        for file in only_in_dir2:
            f.write(f"{file}\n")
            
    print(f"Comparison results saved to {output_file}")

def run_diff(args):
    if not os.path.isdir(args.dir1) or not os.path.isdir(args.dir2):
        print("One or both input directories are invalid.")
        return
    compare_directories(args.dir1, args.dir2, args.out)

def register_parser(subparsers):
    parser = subparsers.add_parser("diff", help="Compare two directories and output unique files.")
    parser.add_argument("--dir1", required=True, help="First directory")
    parser.add_argument("--dir2", required=True, help="Second directory")
    parser.add_argument("--out", default="comparison_results.txt", help="Output file")
    parser.set_defaults(func=run_diff)
