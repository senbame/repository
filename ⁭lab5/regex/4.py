import re
with open(r"⁭lab5/regex/new_row.txt", "r", encoding="utf-8") as file:
    text = file.read()
x = re.search("[A-Z]?[a-z]", text)
if x:
    print("Yes")
else:
    print("No")
x = re.findall("[A-Z][a-z]+",text)
print(x)