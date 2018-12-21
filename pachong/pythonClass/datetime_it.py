import datetime

begin = datetime.datetime.strptime("2018-12-15","%Y-%m-%d")
end = datetime.datetime.strptime("2018-12-18","%Y-%m-%d")

# see https://stackoverflow.com/questions/466345/converting-string-into-datetime
d = begin
delta = datetime.timedelta(days=1)
while d <= end:
    dateStr = d.strftime("%Y-%m-%d")
    print(dateStr)
    d += delta
