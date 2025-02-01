class Account():
    def __init__(self,owner,balance = 0):
        self.owner = owner
        self.balance = balance
    def deposit(self):
        money = int(input("Enter the amount of money that you want to deposit:"))
        self.balance += money
        print(f"Your balance is {self.balance}")
    def withdraw(self):
        if(self.balance == 0):
            print("You don't have any money!")
        else:
            x = int(input("Enter the amount of money that you want to withdraw: "))
            if(self.balance < x):
                print("You don't have such money on your balance")
                print(f"Your balance is {self.balance}")
            else:
                self.balance -= x
                print(f"Your balance is {self.balance}")
p1 = Account("Dastan")
action = input("deposit , withdraw or q to finish: ")
while(action != "q"):
    if(action == "deposit"):
        p1.deposit()
        action = input("deposit , withdraw or q to finish: ")
    elif(action == "withdraw"):
        p1.withdraw()
        action = input("deposit , withdraw or q to finish: ")
else:
    print("Goodbye :) ")
