import os
def check_exist(path):
    if os.path.exists(path):
        print("Filename is:", os.path.basename(path))
        print("Directory is:",os.path.dirname(path))
    else:
        print("No such path")
path = r"C:\KBTU\githowto\PP2"
check_exist(path)

