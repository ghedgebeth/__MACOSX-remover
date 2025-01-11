import os
import zipfile
import shutil
from tkinter import Tk, filedialog

def sanitize_filename(name):
    """Sanitize file or directory names by removing invalid characters."""
    invalid_chars = '<>:"|?*'
    reserved_names = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    name = ''.join(char if char not in invalid_chars else '_' for char in name)
    if name.upper() in reserved_names:
        name += '_safe'
    return name

def sanitize_path(path_parts):
    """Sanitize all parts of a file path."""
    return [sanitize_filename(part) for part in path_parts]

def process_zip_file(zip_path, output_directory):
    # Ensure the ZIP file exists
    if not os.path.isfile(zip_path):
        print(f"Error: The file {zip_path} does not exist.")
        return

    # Get the base name of the ZIP file (without extension)
    zip_name = os.path.splitext(os.path.basename(zip_path))[0]

    # Create the output folder for __MACOSX files
    macosx_folder = os.path.join(output_directory, f"MACOSX-{zip_name}.zip")

    try:
        # Temporary extraction directory
        temp_extract_dir = os.path.join(output_directory, f"temp_{zip_name}")
        os.makedirs(temp_extract_dir, exist_ok=True)

        files_to_keep = {}

        # Open the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Check if __MACOSX exists in the ZIP
            macosx_files = [item for item in zip_ref.namelist() if item.startswith("__MACOSX")]
            if not macosx_files:
                print(f"No __MACOSX folder found in {zip_path}. Skipping extraction.")
                return

            # Extract only __MACOSX files to the temporary directory
            for macosx_file in macosx_files:
                try:
                    sanitized_path = os.path.join(temp_extract_dir, *sanitize_path(macosx_file.split("/")))
                    os.makedirs(os.path.dirname(sanitized_path), exist_ok=True)
                    if not macosx_file.endswith("/"):  # Skip directories
                        with open(sanitized_path, "wb") as f:
                            f.write(zip_ref.read(macosx_file))
                except (OSError, FileNotFoundError) as e:
                    print(f"Skipping problematic file: {macosx_file} - {e}")

            # Collect data for files to keep
            for item in zip_ref.namelist():
                if not item.startswith("__MACOSX"):
                    try:
                        files_to_keep[item] = zip_ref.read(item)
                    except KeyError as e:
                        print(f"Error reading {item} from ZIP: {e}")

            # Create a new ZIP file for the __MACOSX folder
            with zipfile.ZipFile(macosx_folder, 'w') as macosx_zip:
                for macosx_file in macosx_files:
                    sanitized_macosx_path = os.path.join(temp_extract_dir, *sanitize_path(macosx_file.split("/")))
                    if os.path.exists(sanitized_macosx_path):
                        macosx_zip.write(sanitized_macosx_path, macosx_file)

        # Recreate the original ZIP file without the __MACOSX folder
        with zipfile.ZipFile(zip_path, 'w') as new_zip:
            for item, content in files_to_keep.items():
                sanitized_item = '/'.join(sanitize_path(item.split("/")))
                new_zip.writestr(sanitized_item, content)

    except zipfile.BadZipFile:
        print(f"Error: The file {zip_path} is not a valid ZIP file.")
    finally:
        # Clean up the temporary extraction directory
        shutil.rmtree(temp_extract_dir, ignore_errors=True)

    print(f"Processed {zip_path}: __MACOSX files moved to {macosx_folder}, original ZIP updated.")

def process_zip_files_in_directory(directory_path, output_directory):
    # Ensure the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: The directory {directory_path} does not exist.")
        return

    # Find all ZIP files in the directory
    zip_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.zip')]

    # Process each ZIP file
    for zip_file in zip_files:
        process_zip_file(zip_file, output_directory)

def select_directory(prompt):
    Tk().withdraw()  # Hide the root Tkinter window
    return filedialog.askdirectory(title=prompt)

# Interactive interface
if __name__ == "__main__":
    print("Select the directory containing the ZIP files.")
    zip_directory = select_directory("Select ZIP Files Directory")

    print("Select the output directory for extracted files.")
    output_directory = select_directory("Select Output Directory")

    if zip_directory and output_directory:
        process_zip_files_in_directory(zip_directory, output_directory)
    else:
        print("Operation cancelled.")
# The code has been refactored to improve the handling of file names and paths, including sanitization of invalid characters and reserved names. The process_zip_file function now extracts only the __MACOSX files to a temporary directory, while collecting data for the files to keep in the original ZIP. The new ZIP file for the __MACOSX folder is created using sanitized paths, and the original ZIP is recreated without the __MACOSX folder. The code also includes error handling for problematic files and missing items in the ZIP file. The interactive interface allows users to select input and output directories using a file dialog.