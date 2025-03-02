import os
def delete_file(path):
    if os.path.exists(path) and os.access(path , os.W_OK):
        os.remove(path)
        print("File Deleted successfully")
    else:
        print("There is no such path")
l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in l:
    file = (fr"C:\KBTU\githowto\PP2\{i}.txt")
    delete_file(file)