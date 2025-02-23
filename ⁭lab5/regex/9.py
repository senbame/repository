import re
with open(r"⁭lab5/regex/new_row.txt", "r", encoding="utf-8") as file:
    text = file.read()
txt = "HelloWorld"
x = re.sub(r"([A-Z])" , r" \1" , txt)
print(x)