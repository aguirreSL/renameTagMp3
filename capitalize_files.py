import os

# Global directory removed to use argparse

def process_directory(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.m4a'):
            # Split the filename into name and extension
            name, ext = os.path.splitext(filename)
            
            # Capitalize each word in the entire filename (except the extension)
            new_name = ' '.join(word.capitalize() for word in name.split())
            
            # Reconstruct the filename with the extension
            new_filename = f"{new_name}{ext}"
            
            # Get the full paths
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Capitalize words in .m4a filenames.")
    parser.add_argument("--dir", required=True, help="Directory containing .m4a files")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        process_directory(args.dir)
    else:
        print(f"Directory not found: {args.dir}")