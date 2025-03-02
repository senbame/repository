def count_line(file_path):
    text = open(f"{file_path}" , "r" , encoding="utf-8")
    lines = text.readlines()
    text.close()
    return len(lines)
print("Number of lines:" , count_line(r"C:\KBTU\githowto\PP2\lab6\dir_and_files\lab6.txt"))