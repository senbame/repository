import math
n = int(input("Enter a number of sides(at least 4):"))
s = int(input("Enter a length of a side:"))
area = (n * s ** 2) / (4 * math.tan(math.pi / n))
print(area)
