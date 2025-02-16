import datetime
x = datetime.datetime.now()
new_time = x - datetime.timedelta(days=5)
print("Now date is: ",new_time.strftime("%Y-%m-%d"))