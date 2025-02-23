import re
with open(r"⁭lab5/regex/new_row.txt", "r", encoding="utf-8") as file:
    text = file.read()
x = re.sub("[\s,.]" , ":" , text)
print(x)