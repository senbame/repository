def squares(n):
    for i in range(1,n+1):
        yield i**2
x = int(input())
for i in squares(x):
    print(i)

