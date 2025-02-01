import math
def volum_of_sphere(r):
    v = 4/3 * math.pi * r**3
    print(v)
radius = int(input())
volum_of_sphere(radius)