import os

def list_files_with_copy(directory):
    """
    Lists files in the specified directory that contain the word "copy" in their title.
    """
    files_with_copy = []

    # Traverse the directory
    for filename in os.listdir(directory):
        # Check if "copy" is in the filename (case-insensitive)
        if "2." in filename.lower():
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            files_with_copy.append(file_path)
    
    return files_with_copy

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find files with 'copy' or '2.' in their names.")
    parser.add_argument("--dir", required=True, help="Directory to search")
    parser.add_argument("--out", default="files_with_copy.txt", help="Output file name")
    args = parser.parse_args()
    
    if os.path.exists(args.dir):
        # Get the list of files with "copy" in the title
        files_with_copy = list_files_with_copy(args.dir)
        
        # Sort the list alphabetically
        files_with_copy.sort()
        
        # Write the results to the text file
        with open(args.out, "w") as file:
            if files_with_copy:
                file.write("Files with 'copy' in the title (sorted alphabetically):\n")
                for file_path in files_with_copy:
                    file.write(file_path + "\n")
            else:
                file.write("No files with 'copy' in the title found.\n")
        
        print(f"Results saved to {args.out}")
    else:
        print(f"The directory {args.dir} does not exist.")