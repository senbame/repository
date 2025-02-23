import re
with open(r"⁭lab5/regex/new_row.txt", "r", encoding="utf-8") as file:
    text = file.read()
txt = "camel_snake"
x = re.sub("_[a-z]" , lambda m : m.group(0)[1].upper(), txt)
print(x)