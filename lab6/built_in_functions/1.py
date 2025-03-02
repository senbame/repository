from functools import reduce
def multi_list(n):
    return reduce(lambda a , b : a * b , n)
list = [1,2,3,4,5,6,7]
print(multi_list(list))