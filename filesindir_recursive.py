import pathlib
import itertools
from functools import wraps

def validate_path(func):
    """Decorator to validate directory exists before processing."""
    @wraps(func)
    def wrapper(directory, extension, depth=0):
        if not directory.exists():
            print(f"❌ Directory {directory} does not exist - skipping")
            return
        if not directory.is_dir():
            print(f"❌ {directory} is not a directory - skipping")
            return
        return func(directory, extension, depth)
    return wrapper

def validate_extension(func):
    """Decorator to validate extension is a known file type."""
    KNOWN_EXTENSIONS = {
        '.txt', '.docx', '.pdf', '.py', '.md', '.csv', '.xlsx',
        '.jpg', '.png', '.gif', '.mp4', '.mp3', '.zip', '.json'
    }

    @wraps(func)
    def wrapper(directory, extension, depth=0):
        if extension.lower() not in KNOWN_EXTENSIONS:
            print(f"⚠️  Unknown extension '{extension}' - skipping")
            return
        return func(directory, extension, depth)
    return wrapper

def print_list(label, items):
    """Print a list of items with a label."""
    if items:
        print(f"{label}:\n {', '.join(items)}")
    else:
        print(f"{label}:\n None found")

def get_files_by_extension(directory, extension, depth=0):
    """Get files with specified extension from directory with depth control."""
    if depth == 0:
        # Current directory only
        return list(directory.glob(f"*{extension}"))
    elif depth == -1:
        # Unlimited recursion
        return list(directory.rglob(f"*{extension}"))
    else:
        # Limited depth recursion
        files = []
        
        def collect_files(current_dir, current_depth, max_depth):
            try:
                # Get files in current directory
                files.extend(current_dir.glob(f"*{extension}"))
                
                # If we haven't reached max depth, recurse into subdirectories
                if current_depth < max_depth:
                    for subdir in current_dir.iterdir():
                        if subdir.is_dir():
                            collect_files(subdir, current_depth + 1, max_depth)
            except (PermissionError, OSError):
                # Gracefully handle permission errors
                pass
        
        collect_files(directory, 0, depth)
        return files

@validate_path
@validate_extension
def process_and_print_files(directory, extension, depth=0):
    """Process files in directory and print both names and stems."""
    files = get_files_by_extension(directory, extension, depth)
    files_with_ext = [f.name for f in files]
    file_stems = [f.stem for f in files]
    
    depth_desc = {
        0: "current directory only",
        -1: "unlimited recursion",
    }
    depth_text = depth_desc.get(depth, f"{depth} levels deep")
    
    print(f"\nFiles in {directory} with extension {extension} ({depth_text}):")
    print_list("files with extensions", files_with_ext)
    print_list("file stems", file_stems)

def scan_directories(dir_depth_pairs, extensions):
    """Scan all combinations of directories/depths and extensions."""
    for (directory, depth), extension in itertools.product(dir_depth_pairs, extensions):
        process_and_print_files(directory, extension, depth)

# Define directories with individual depth settings
directories = [
    (pathlib.Path.home() / "Documents", 0),    # Current directory only
    (pathlib.Path.home() / "Downloads", 2),   # 2 levels deep
    (pathlib.Path.home() / "Desktop", -1)     # Unlimited recursion
]

extensions = [".docx", ".txt", ".pdf"]

# Process all combinations with depth control
# depth=0: current directory only
# depth=1,2,3,etc: that many levels deep
# depth=-1: unlimited recursion
scan_directories(directories, extensions)