from pathlib import Path
from config import (
    RAW_DIR,
    PROCESSED_DIR,
    SAMPLE_DIR,
    MASTER_DIR,
    QUALITY_DIR
)

def create_project_folders() -> None:
    """
    Create project folders if they do not exist.
    """
    folders = (RAW_DIR, PROCESSED_DIR, SAMPLE_DIR, MASTER_DIR,QUALITY_DIR)

    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)


def get_files_by_extension(folder_path: Path, ext: str) -> list[Path]:
    """
    Return files in a folder that match the given extension.
    """

    if not ext:
        raise ValueError(f"Extension must be provided.")
    
    return [
        file_path
        for file_path in folder_path.iterdir()
        if file_path.is_file() and file_path.suffix[1:] == ext
    ]


def remove_files(path:Path, ext:str = "", is_missing_ok: bool = True) -> list[Path]:
    """
    Remove a single file or all files with a given extension from a folder.

    Parameters
    ----------
    path : Path
        Path to a file or folder.
    ext : str, optional
        File extension to filter by, with or without a leading dot.
        Required when `path` is a folder.
    missing_ok : bool, optional
        If True, return an empty list when the path does not exist.

    Returns
    -------
    list[Path]
        Paths of the files that were removed.
    """
    is_folder = path.is_dir()
    is_file = path.is_file()
    ext = ext.lstrip(".")

    if not (is_file or is_folder):
        if is_missing_ok:
            return []

        raise ValueError(f"{path} doesn't exists")
    
    if is_folder:            
        files_to_remove = get_files_by_extension(path, ext)

        for file_path in files_to_remove:
            file_path.unlink()

        return files_to_remove
    
    if is_file:
        if ext and path.suffix[1:] != ext:
            raise ValueError(f"File extension does not match the provided extension")

        path.unlink()
        return [path]
