import datetime
x = datetime.datetime.now()
yesterday = x - datetime.timedelta(days = 1)
tomorrow = x + datetime.timedelta(days = 1)
print("Yesterday was:",yesterday.strftime("%Y-%m-%d"))
print("Today is",x.strftime("%Y-%m-%d"))
print("Tomorrow will be:",tomorrow.strftime("%Y-%m-%d"))