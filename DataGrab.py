import twint
import datetime

def DataGrab(startDate,endDate):
    c = twint.Config()
    c.Popular_tweets = True
    c.Since = startDate
    c.Until = endDate
    c.Search = "#Bitcoin OR $BTC"
    c.Custom["user"] = ["id", "username"]
    c.Limit = 10000
    c.Store_csv = True
    c.Output = startDate[0:10]
    twint.run.Search(c)

startDate = datetime.datetime(2020,3,20)
while startDate!=datetime.datetime(2021,3,16):
    endDate = startDate + datetime.timedelta(days=3)
    DataGrab(str(startDate),str(endDate))
    startDate += datetime.timedelta(days=1)
