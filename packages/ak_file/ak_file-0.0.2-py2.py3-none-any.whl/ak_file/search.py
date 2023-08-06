from pathlib import Path
from typing import Generator

def find_files_w_extension(folder_path:str, extension:str, search_subdir:bool=False) -> Generator[Path, None, None]:
    "Returns a list of files in the directory with matching extension"
    return Path(folder_path).glob(f"{'**/' if search_subdir else ''}*.{extension}")