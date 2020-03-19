import os
from pathlib import Path
from typing import List, Tuple
import datetime

from emeki.util import create_dir

DATA_DIR = os.path.join(Path(__file__).parent, "project_templates")

Rule_T = List[Tuple[str, str]]


def repl_in_str(s: str, rep_rules: Rule_T) -> str:
    """Applies a series of replacements to a string."""
    contents = s
    for s1, s2 in rep_rules:
        contents = contents.replace(s1, s2)
    return contents


def repl_in_file(file_path: str, dest_path: str, rep_rules: Rule_T) -> None:
    """Applies a set of replacements to the specified file's content.

    And saves it at `dest_path`."""
    with open(file_path, "r") as f:
        contents = f.read()

    contents = repl_in_str(contents, rep_rules)

    with open(dest_path, "w") as f:
        f.write(contents)


def copy_and_modify_recursive(
    curr_path: str, curr_target_dir: str, rep_rule: Rule_T
) -> None:
    """Copies a folder recursively and applies renaming."""
    if os.path.isdir(curr_path):
        create_dir(curr_target_dir)
        for f in os.listdir(curr_path):
            f_path = os.path.join(curr_path, f)
            f_mod = repl_in_str(f, rep_rule)
            next_target_dir = os.path.join(curr_target_dir, f_mod)
            copy_and_modify_recursive(f_path, next_target_dir, rep_rule)
    else:
        if curr_path.split(".")[-1] in ["py", "in", "txt", "rst", "md", "gitignore", "LICENSE", "ps1"]:
            # print(curr_path)
            repl_in_file(curr_path, curr_target_dir, rep_rule)
            # TODO: Include images, but copy only!


def setup_project(target_dir: str, project_name: str, author: str):
    """Sets up a sample project."""
    project_name_under = project_name.replace("-", "_")
    rep_rules = [
        ("PROJECT_NAME_UNS", project_name_under),
        ("PROJECT_NAME", project_name),
        ("AUTHOR", author),
        ("CURRENT_YEAR", f"{datetime.datetime.now().year}"),
    ]
    copy_and_modify_recursive(DATA_DIR, target_dir, rep_rules)
