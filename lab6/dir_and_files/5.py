def list_to_file(path , list):
    text = open(f"{path}" , "w", encoding="utf-8")
    text.writelines(list)
    text.close()
l = ["hello ", "hi" , "bye"]
list_to_file(r"C:\KBTU\githowto\PP2\lab6\dir_and_files\lab6.txt", l)


