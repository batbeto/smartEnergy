import datetime as dt

a = dt.date(2019,02,04)
b = "{}-{}-{}T02:45:00".format(a.year,a.month,a.day +1)
b = dt.datetime.strptime(b, "%Y-%m-%dT%H:%M:%S")
print(b.timestamp())
