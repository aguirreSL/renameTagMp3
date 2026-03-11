import os

def generate_list(folder_path, output_file):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    
    # Filter out only files (excluding directories)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    
    # Write the list of files to the text file
    with open(output_file, 'w') as file:
        for song in files:
            file.write(song + '\n')
    
    print(f"List of songs saved to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate a text list of all files in a directory.")
    parser.add_argument("--dir", required=True, help="Directory to scan")
    parser.add_argument("--out", default="./song_list.txt", help="Output text file path")
    args = parser.parse_args()
    
    if os.path.isdir(args.dir):
        generate_list(args.dir, args.out)
    else:
        print(f"The directory {args.dir} does not exist.")