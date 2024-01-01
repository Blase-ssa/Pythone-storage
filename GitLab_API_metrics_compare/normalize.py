#!/usr/bin/env python3
import json
from globals import *


def normalize_json_file(filename):
    """Loads a json file into memory and uploads the data back in a normalized form."""
    print(f'processing "{filename}"')
    with open(filename, "r", encoding="utf-8") as file:
        file_contents = json.load(file)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(file_contents, indent=2))


def normalize_json_dir(dirname):
    """Iterates through all the files in a directory and normalizes them."""
    file_list = get_files(dirname)
    for filename in file_list:
        normalize_json_file(filename)


if __name__ == "__main__":
    normalize_json_dir(RESTORED_USR_DIR)
    normalize_json_dir(RESTORED_PROJECT_DIR)
    normalize_json_dir(PROD_USR_DIR)
    normalize_json_dir(PROD_PROJECT_DIR)
