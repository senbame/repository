def gen_files():
    l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in l:
        f = f"{i}.txt"
        with open(f , "w" ) as file:
            file.write(f"This is {file.name} file")
gen_files()