class first():
    def __init__(self):
        self.string = ""
    def getString(self):
        self.string = input("Enter a string:")
    def printString(self):
        print("Your string is: "+self.string)

p1 = first()
p1.getString()
p1.printString()
