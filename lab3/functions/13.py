from random import randint
def guess_a_number():
    random_number = randint(1,20)
    print("Hello! What is your name")
    name = input()
    print((f"Well, {name} , I am thinking of a number between 1 and 20"))
    print("Take a guess")
    number = int(input())
    count = 0
    while(number != random_number):
        if(number > random_number):
            print("Your guess is too high")
            count += 1
            print("Take a guess")
            number = int(input())
        elif(number < random_number):
            print("Your guess is too low")
            count += 1
            print("Take a guess")
            number = int(input())
    else:
        print(f"Good job , {name}! You guessed a number in {count} guesses!")
guess_a_number()