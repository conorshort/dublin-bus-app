import datetime
t = '24:15:00'
d = datetime.datetime.strptime(t, "%H:%M:%S")
print(d)
