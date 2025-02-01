from itertools import permutations 
def permut():
    x = input()
    list = permutations(x)
    for i in list:
        print("".join(i))
    

permut()