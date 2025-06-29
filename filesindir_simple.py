import pathlib

# helper function to keep the ugly join out of the main code
def print_list(label, items):
    if items:
        print(f"{label}:\n {', '.join(items)}")
    else:
        print(f"{label}:\n None found")

# path to directory of interest
dir_of_interest = pathlib.Path.home() / "Documents"

# extension of interest
ext_of_interest = ".pdf"

# file names with extensions
files_with_ext = [f.name for f in dir_of_interest.glob(f"*{ext_of_interest}")]
# file names without extensions
file_stems = [f.stem for f in dir_of_interest.glob(f"*{ext_of_interest}")]

# print the results
print(f"Files in {dir_of_interest} with extension {ext_of_interest}:")
print_list("Files with extension", files_with_ext)
print_list("File stems", file_stems)