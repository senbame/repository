import math
class Point():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def show(self):
        print("Your x coordinate: " + str(self.x))
        print("Your y coordinate: " + str(self.y))
        print("Your z coordinate: " + str(self.z))
    def move(self,first,second,third):
        print(f"Your x coordinate moved to {first}")
        print(f"Your y coordinate moved to {second}")
        print(f"Your z coordinate moved to {third}")
        self.x = first
        self.y = second
        self.z = third
    def dist(self, second_point):
        return math.sqrt((self.x - second_point.x) ** 2 + (self.y - second_point.y) ** 2 + (self.z - second_point.z)**2)

p1 = Point(5,6,7)
p2 = Point(8,5,6)
p1.show()
p1.move(6,8,5)
print("The Distance is : ", p1.dist(p2))