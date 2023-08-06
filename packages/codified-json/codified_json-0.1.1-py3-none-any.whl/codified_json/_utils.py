import os

def create_file_path(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
