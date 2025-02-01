from math import sqrt
lst = map(int,input().split())
lst = list(lst)
def prime_numbers(x):
    if x < 2:
        return False
    for i in range(2 , int(sqrt(x))+1):
        if x % i == 0:
            return False
    return True
new_list = list((filter(lambda x : prime_numbers(x), lst)))
print(new_list)