def reverseble(n):
    for i in reversed(range(0,n+1)):
        yield i
x = int(input())
for i in reverseble(x):
    print(i)