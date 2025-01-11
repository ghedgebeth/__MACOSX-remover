# __MACOSX-remover
Separates the " __MACOSX" folder and its contents to a separate directory in bulk music pack zip files.    


This Python script processes ZIP files by isolating and extracting __MACOSX folders, sanitizing filenames and paths, and updating the original ZIP files to remove the __MACOSX folders. It creates a new ZIP archive for the extracted __MACOSX content and ensures that all operations handle file naming and pathing issues safely.

Features:

Extracts __MACOSX folders from ZIP files.
Sanitizes filenames and file paths to remove invalid or reserved characters.
Creates a new ZIP archive for the extracted __MACOSX folder.
Updates the original ZIP file by removing the __MACOSX folder and keeping the rest of the content intact.
Provides an interactive GUI to select input and output directories using Tkinter.

Requirements:
Python 3.6 or higher
tkinter module (comes pre-installed with most Python distributions)

Installation:
Clone or download the repository containing this script.
Ensure Python 3.6 or higher is installed on your system.

Usage:

Run the script:

python process_zip_files.py
Select the directory containing ZIP files when prompted.
Select the output directory where the processed files will be saved.

The script will:
Process each ZIP file in the selected directory.
Extract and save __MACOSX folders as new ZIP files in the output directory.
Update the original ZIP files to remove __MACOSX folders.
Code Details
Key Functions

sanitize_filename(name):
Cleans filenames by replacing invalid characters and handling reserved names.
sanitize_path(path_parts):
Applies sanitize_filename to all components of a file path.
process_zip_file(zip_path, output_directory):
Handles the processing of a single ZIP file, including extraction, sanitization, and updating.
process_zip_files_in_directory(directory_path, output_directory):
Processes all ZIP files in a specified directory.
select_directory(prompt):
Provides a GUI interface to select directories interactively.

Workflow
Extracts only the __MACOSX folder from a ZIP file.
Sanitizes file names and paths during extraction.
Saves the __MACOSX content as a new ZIP file in the output directory.

Recreates the original ZIP file without the __MACOSX folder.
Cleans up temporary files and directories.

Example:

Input Directory

example.zip

Contains:
__MACOSX/
Other files and folders.

Output Directory
MACOSX-example.zip:
Contains only the __MACOSX folder from example.zip.

Updated example.zip:
Contains all original files except the __MACOSX folder.

Notes
Ensure the input ZIP files are valid and accessible.
The script will skip files that cannot be processed due to errors.
Original ZIP files are updated in place; consider backing them up if needed.


License

This script is provided as-is and is free to use and modify. 

