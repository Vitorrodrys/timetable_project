import argparse
from pathlib import Path

def dir_path(path_str: str) -> Path:
    p = Path(path_str)
    if not p.exists():
        raise argparse.ArgumentTypeError(f"Path '{path_str}' does not exist.")
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f"Path '{path_str}' is not a directory.")
    return p

def file_path(path_str: str) -> Path:
    p = Path(path_str)
    if not p.exists():
        raise argparse.ArgumentTypeError(f"File '{path_str}' does not exist.")
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"Path '{path_str}' is not a file.")
    return p
