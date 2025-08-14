import os
import sys

def resource_path(relative_path):
    try:
        #this needs to be here for grabbing pyinstaller file
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_words(filepath):
    full_path = resource_path(filepath)
    with open(full_path, "r") as f:
        return [line.strip() for line in f if line.strip()]
