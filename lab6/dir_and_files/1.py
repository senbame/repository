import os
def list_items(path):
    print("Directories:", [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    print("Files:", [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    print("All Items:", os.listdir(path))

path = r"C:\KBTU\githowto\PP2"
list_items(path)