from pathlib import Path

def find_media_files(start_path):
    """Find media files in the specified directory."""
    media_extensions = (
    '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', 
    '.wma', '.mp2', '.mp4', '.avi', '.mov', '.wmv', 
    '.mkv', '.webm', '.opus', '.aiff', '.dsd', '.m4b'
)
    media_files = []

    for path in Path(start_path).rglob("*"):
        if path.is_file() and path.suffix.lower() in media_extensions:
            media_files.append(str(path))
    
    return media_files

def delete_file(file_path):
    """Delete the specified file."""
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

def main():
    home_directory = '/home'
    media_files = find_media_files(home_directory)

    if not media_files:
        print("No media files found in the /home directory.")
        return

    print(f"Found {len(media_files)} media file(s).")
    for media_file in media_files:
        user_input = input(f"MEDIA FILE: {media_file}\nDelete this file? (Y/n): ").strip().lower()
        if user_input == 'y' or user_input == 'yes':
            delete_file(media_file)
        else:
            print(f"Continuing with {media_file} intact.")

if __name__ == "__main__":
    main()
