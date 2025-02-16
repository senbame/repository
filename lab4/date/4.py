import datetime
x = datetime.datetime.now()
y = datetime.datetime(2020 , 5 , 17)
first = x.timestamp()
second = y.timestamp()
print(first)
print(second)
print(first - second)