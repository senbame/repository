fruits = ["apple", "banana", "cherry", "kiwi", "mango"]

newlist = [x for x in fruits if "a" in x]

print(newlist)
#newlist = [expression for item in iterable if condition == True]
newlist1 = [x for x in fruits if x != "apple"]
newlist2 = [x if x != "banana" else "orange" for x in fruits]
print(newlist2)