import twint
import datetime

def DataGrab(startDate,endDate):
    c = twint.Config()
    c.Popular_tweets = True
    c.Since = startDate
    c.Until = endDate
    c.Search = "#Bitcoin"
    c.Custom["user"] = ["id", "username"]
    c.Limit = 10000
    c.Store_csv = True
    c.Output = startDate[0:10]
    twint.run.Search(c)

startDate = datetime.datetime(2021,1,14)
while startDate!=datetime.datetime(2021,3,14):
    endDate = startDate + datetime.timedelta(days=3)
    print(startDate)
    startDate += datetime.timedelta(days=1)
    DataGrab(str(startDate),str(endDate))
