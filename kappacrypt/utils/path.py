import os

def ensure_valid_keypaths(paths):
    for name, path in paths.items():
        if not os.path.isfile(path):
            raise FileNotFoundError("Invalid path to " + name)