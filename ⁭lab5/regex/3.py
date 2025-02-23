import re
with open(r"⁭lab5/regex/new_row.txt", "r", encoding="utf-8") as file:
    text = file.read()
x = re.search("[a-z]+_[a-z]", text)
if x:
    print("There is")
else:
    print("There isn't")
y = re.findall("[a-z]+_[a-z]",text)
print(y)