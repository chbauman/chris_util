"""The util module.

This module provides some utility functionality.
"""
import os
import shutil
import zipfile


def str2bool(v) -> bool:
    """Converts a string to a boolean.

    Raises:
        ValueError: If it cannot be converted.
    """
    if isinstance(v, bool):
        return v
    elif isinstance(v, str):
        v_low = v.lower()
        if v_low in ("yes", "true", "t", "y", "1", "1.0"):
            return True
        elif v_low in ("no", "false", "f", "n", "0", "0.0"):
            return False
    raise ValueError(f"{v} is not convertible to boolean!")


def create_dir(dir_name: str) -> None:
    """Creates the given directory recursively.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return


def zip_dir(dir_path: str, save_path: str):
    """Zips and saves a directory."""
    shutil.make_archive(save_path, 'zip', dir_path)


def unzip_to(file_to_unzip: str, dest_dir: str):
    """Extract all the contents of zip file in `dest_dir`."""
    with zipfile.ZipFile(file_to_unzip, 'r') as zipObj:
        zipObj.extractall(dest_dir)


def emeki_main():
    """The main function.

    It may be called directly from the command line when
    typing `emeki`."""
    print("Hoi! This is my personal python library.")
