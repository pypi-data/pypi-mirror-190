from ak_file.search import *
from pathlib import Path

parent_dir = Path(__file__).parent.parent

def test_find_files_w_extension():
    assert len(list(find_files_w_extension(parent_dir, 'py', False))) == 0
    assert len(list(find_files_w_extension(parent_dir, 'toml', False))) == 1