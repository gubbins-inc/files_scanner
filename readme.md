# From Simple to Sophisticated: Building a Python File Scanner

This tutorial shows how to evolve a simple file listing script into a powerful, flexible tool through incremental improvements. We'll start with basic functionality and gradually add features while maintaining clean, readable code.

## Step 1: The Simple Beginning

Let's start with the most basic approach - listing files of a specific type:

import pathlib

# Simple approach - hardcoded values
desktop = pathlib.Path.home() / "Desktop"
txt_files = [f.name for f in desktop.glob("*.txt")]
print(txt_files)

**Problems with this approach:**
- Hardcoded directory and file type
- Ugly list output with brackets
- Not reusable

## Step 2: Clean Up the Output

First, let's make the output more readable:

```python
import pathlib

desktop = pathlib.Path.home() / "Desktop"
txt_files = [f.name for f in desktop.glob("*.txt")]

# Pretty print without brackets
print("TXT files:", *txt_files, sep=', ') if txt_files else print("TXT files: None found")
```

**Improvement:** Clean output, but still not very reusable.

## Step 3: Extract File Names Without Extensions

Often we want just the filename without the extension:

```python
import pathlib

desktop = pathlib.Path.home() / "Desktop"

# Get both names and stems
files = list(desktop.glob("*.txt"))
files_with_ext = [f.name for f in files]
file_stems = [f.stem for f in files]

print("Files with extensions:", *files_with_ext, sep=', ') if files_with_ext else print("Files with extensions: None found")
print("File stems:", *file_stems, sep=', ') if file_stems else print("File stems: None found")
```

**Problem:** The output formatting is getting ugly and repetitive.

## Step 4: Create Helper Functions

Let's hide the ugly `join()` logic in a helper function:

```python
import pathlib

def print_list(label, items):
    """Print a list of items with a label."""
    if items:
        print(f"{label}:\n {', '.join(items)}")
    else:
        print(f"{label}:\n None found")

desktop = pathlib.Path.home() / "Desktop"

files = list(desktop.glob("*.txt"))
files_with_ext = [f.name for f in files]
file_stems = [f.stem for f in files]

print_list("Files with extensions", files_with_ext)
print_list("File stems", file_stems)
```

**Improvement:** Much cleaner! The ugly formatting logic is hidden away.

## Step 5: Make It Configurable

Now let's make the directory and file type configurable:

```python
import pathlib

def print_list(label, items):
    """Print a list of items with a label."""
    if items:
        print(f"{label}:\n {', '.join(items)}")
    else:
        print(f"{label}:\n None found")

def get_files_by_extension(directory, extension):
    """Get files with specified extension from directory."""
    return list(directory.glob(f"*{extension}"))

# Configuration
dir_of_interest = pathlib.Path.home() / "Documents"
ext_of_interest = ".docx"

# Process files
files = get_files_by_extension(dir_of_interest, ext_of_interest)
files_with_ext = [f.name for f in files]
file_stems = [f.stem for f in files]

# Display results
print(f"Files in {dir_of_interest} with extension {ext_of_interest}:")
print_list("Files with extensions", files_with_ext)
print_list("File stems", file_stems)
```

**Improvement:** Now we can easily change what we're looking for!

## Step 6: Handle Multiple Directories and File Types

What if we want to scan multiple directories for multiple file types?

```python
import pathlib
import itertools

def print_list(label, items):
    """Print a list of items with a label."""
    if items:
        print(f"{label}:\n {', '.join(items)}")
    else:
        print(f"{label}:\n None found")

def get_files_by_extension(directory, extension):
    """Get files with specified extension from directory."""
    return list(directory.glob(f"*{extension}"))

def process_and_print_files(directory, extension):
    """Process files in directory and print both names and stems."""
    files = get_files_by_extension(directory, extension)
    files_with_ext = [f.name for f in files]
    file_stems = [f.stem for f in files]
    
    print(f"\nFiles in {directory} with extension {extension}:")
    print_list("Files with extensions", files_with_ext)
    print_list("File stems", file_stems)

def scan_directories(directories, extensions):
    """Scan all combinations of directories and extensions."""
    for directory, extension in itertools.product(directories, extensions):
        process_and_print_files(directory, extension)

# Configuration
directories = [
    pathlib.Path.home() / "Documents",
    pathlib.Path.home() / "Downloads", 
    pathlib.Path.home() / "Desktop"
]

extensions = [".docx", ".txt", ".pdf", ".py"]

# Process all combinations
scan_directories(directories, extensions)
```

**Improvement:** Now we can scan multiple directories for multiple file types with one call! The `itertools.product()` creates all combinations automatically.

## Step 7: Add Error Handling with Decorators

Real-world file operations can fail. Let's add robust error handling using decorators:

```python
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
    print_list("Files with extensions", files_with_ext)
    print_list("File stems", file_stems)

def scan_directories(directories, extensions):
    """Scan all combinations of directories and extensions."""
    for directory, extension in itertools.product(directories, extensions):
        process_and_print_files(directory, extension)

# Configuration
directories = [
    pathlib.Path.home() / "Documents",
    pathlib.Path.home() / "Downloads", 
    pathlib.Path.home() / "Desktop"
]

extensions = [".docx", ".txt", ".pdf", ".py"]

# Process all combinations
scan_directories(directories, extensions)
```

**Improvement:** Now the script gracefully handles missing directories and unknown file extensions without crashing.

## Step 8: Add Flexible Recursion Control

Finally, let's add the ability to control how deep we search in each directory:

```python
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
    print_list("Files with extensions", files_with_ext)
    print_list("File stems", file_stems)

def scan_directories(dir_depth_pairs, extensions):
    """Scan all combinations of directories/depths and extensions."""
    for (directory, depth), extension in itertools.product(dir_depth_pairs, extensions):
        process_and_print_files(directory, extension, depth)

# Configuration with per-directory depth control
directories = [
    (pathlib.Path.home() / "Documents", 0),    # Current directory only
    (pathlib.Path.home() / "Downloads", 2),   # 2 levels deep
    (pathlib.Path.home() / "Desktop", -1)     # Unlimited recursion
]

extensions = [".docx", ".txt", ".pdf", ".py"]

# Process all combinations
scan_directories(directories, extensions)
```

## Key Learning Points

### 1. **Start Simple, Evolve Gradually**
We began with a 3-line script and gradually added features. Each step solved a real problem while maintaining readability.

### 2. **Extract Functions Early**
As soon as we had repetitive code, we extracted it into functions. This made the code more maintainable and testable.

### 3. **Use Decorators for Cross-Cutting Concerns**
Error handling and validation are perfect candidates for decorators. They keep the main logic clean while adding robustness.

### 4. **Leverage Python's Standard Library**
- `pathlib` for cross-platform path handling
- `itertools.product()` for generating combinations
- `functools.wraps` for proper decorator implementation

### 5. **Configuration Over Hard-Coding**
Moving from hardcoded values to configurable parameters made the tool much more flexible.

### 6. **Graceful Error Handling**
Real-world file operations fail. Our final version handles missing directories, permission errors, and invalid extensions gracefully.

## The Evolution Summary

| Step | Lines of Code | Key Feature Added |
|------|---------------|-------------------|
| 1 | 4 | Basic file listing |
| 2 | 6 | Clean output formatting |
| 3 | 10 | File stems extraction |
| 4 | 15 | Helper functions |
| 5 | 25 | Configurable parameters |
| 6 | 40 | Multiple directories/extensions |
| 7 | 65 | Error handling with decorators |
| 8 | 95 | Flexible recursion control |

Each step added real value while keeping the code maintainable. This approach - starting simple and evolving gradually - is a powerful way to build robust tools without getting overwhelmed by complexity upfront.