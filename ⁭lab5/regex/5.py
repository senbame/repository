import re
with open(r"⁭lab5/regex/new_row.txt", "r", encoding="utf-8") as file:
    text = file.read()
x = re.search("a.*b$",text)
if x:
    print("yes")
else:
    print("no")
x = re.findall("a.*b$",text)
print(x)