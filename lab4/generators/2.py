def even_number(n):
    for i in range(0,n+1):
        if(i%2==0):
            yield i
x = int(input())
for i in even_number(x):
    print(i)