import pathlib
import itertools
from functools import wraps

def validate_path(func):
    """Decorator to validate directory exists before processing."""
    @wraps(func)
    def wrapper(directory, extension):
        if not directory.exists():
            print(f"❌ Directory {directory} does not exist - skipping")
            return
        if not directory.is_dir():
            print(f"❌ {directory} is not a directory - skipping")
            return
        return func(directory, extension)
    return wrapper


def validate_extension(func):
    """Decorator to validate extension is a known file type."""
    KNOWN_EXTENSIONS = {
        '.txt', '.docx', '.pdf', '.py', '.md', '.csv', '.xlsx',
        '.jpg', '.png', '.gif', '.mp4', '.mp3', '.zip', '.json'
    }

    @wraps(func)
    def wrapper(directory, extension):
        if extension.lower() not in KNOWN_EXTENSIONS:
            print(f"⚠️  Unknown extension '{extension}' - skipping")
            return
        return func(directory, extension)
    return wrapper


def print_list(label, items):
    """Print a list of items with a label."""
    if items:
        print(f"{label}:\n {', '.join(items)}")
    else:
        print(f"{label}:\n None found")

def get_files_by_extension(directory, extension):
    """Get files with specified extension from directory."""
    return list(directory.glob(f"*{extension}"))

@validate_path
@validate_extension
def process_and_print_files(directory, extension):
    """Process files in directory and print both names and stems."""
    files = get_files_by_extension(directory, extension)
    files_with_ext = [f.name for f in files]
    file_stems = [f.stem for f in files]
    
    print(f"\nFiles in {directory} with extension {extension}:")
    print_list("files with extensions", files_with_ext)
    print_list("file stems", file_stems)

def scan_directories(directories, extensions):
    """Scan all combinations of directories and extensions."""
    for directory, extension in itertools.product(directories, extensions):
        process_and_print_files(directory, extension)

# Define directories and extensions separately
directories = [
    pathlib.Path.home() / "Documents",
    pathlib.Path.home() / "Downloads", 
    pathlib.Path.home() / "Desktop"
]

extensions = [".docx", ".txt", ".pdf", ".pyx"]

# Process all combinations (3 directories × 4 extensions = 12 combinations)
scan_directories(directories, extensions)