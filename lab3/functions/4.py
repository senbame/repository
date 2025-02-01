num = map(int, input().split())
l = list(num)
def is_prime(int):
    count = 0
    for i in range(1 , int+1):
        if(int % i == 0):
            count += 1
        
    if(count == 2):
        return True
    
    return False
def filter_prime(n):
    lst = []
    for i in n:
        if(is_prime(i)):
            lst.append(i)
    print(sorted(lst))
filter_prime(l)