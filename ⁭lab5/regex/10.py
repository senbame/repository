import re
txt = "HelloWorld"
x = re.sub(r"([A-Z])" , r"_\1",txt).lower().lstrip("_")
print(x)