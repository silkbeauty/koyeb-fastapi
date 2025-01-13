from pathlib import Path
from typing import List


def clean_files(folder_path: str) -> List[str]:
    folder_path = Path(folder_path)
    if not folder_path.exists() or not folder_path.is_dir():
        raise FileNotFoundError(f"Folder {folder_path} not found.")
    
    folder_name = folder_path.name
    
    try:
        base_number = int(folder_name[:6]) * 1000
    except ValueError:
        raise ValueError("Folder name must start with at least 6 digits.")
    
    counter = base_number + 1

    for file in folder_path.iterdir():
        if file.is_file():
            if file.name[:6].isdigit() and file.name[:6] == folder_name[:6]:
                continue
            new_name = file.name.replace("_", " ").replace("-", " ")
            new_name_with_prefix = f"{counter} {new_name}"
            counter += 1  # Increment the counter for the next file

            new_file_path = folder_path / new_name_with_prefix
            file.rename(new_file_path)

    return [file.name for file in folder_path.iterdir() if file.is_file()]
