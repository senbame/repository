def three_and_four(n):
    for i in range(0,n+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
x = int(input())
for i in three_and_four(x):
    print(i)
