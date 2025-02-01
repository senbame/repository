class Shape():
    def __init__(self,length,width):
        self.length = length
        self.width = width
    def area(self):
        return 0
class Rectangle(Shape):
    def __init__(self,length,width):
        super().__init__(length,width)
    def area(self):
        return self.length * self.width 
p1 = Rectangle(int(input("Enter a length:")), int(input("Enter a width:")))
print(p1.area())