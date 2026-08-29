from pathlib import Path

def remove_files(path:Path, ext:str = "") -> list[Path]:
    """
    Remove a single file or all files with a given extension from a folder.

    Parameters
    ----------
    path : Path
        Path to a file or folder.
    ext : str, optional
        File extension to filter by, with or without a leading dot.
        Required when `path` is a folder.

    Returns
    -------
    list[Path]
        Paths of the files that were removed.
    """
    is_folder = path.is_dir()
    is_file = path.is_file()
    ext = ext.lstrip(".")

    if not (is_file or is_folder):
        raise ValueError(f"{path} doesn't exists")
    
    if is_folder:
        if not ext:
            raise ValueError(f"Extension must be provided when removing multiple files from a folder.")
            
        files_to_remove = [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file() and file_path.suffix[1:] == ext
        ]

        for file_path in files_to_remove:
            file_path.unlink()

        return files_to_remove
    
    if is_file:
        if ext and path.suffix[1:] != ext:
            raise ValueError(f"File extension does not match the provided extension")

        path.unlink()
        return [path]
