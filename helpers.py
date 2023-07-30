import os

def count_files_recursive(folder_path):
    """Counts the number of files in the given directory and returns count and file paths."""
    if not os.path.exists(folder_path):
        raise ValueError(f"The folder '{folder_path}' does not exist.")

    if not os.path.isdir(folder_path):
        raise ValueError(f"'{folder_path}' is not a folder.")

    file_count = 0
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)

    return file_count, file_paths