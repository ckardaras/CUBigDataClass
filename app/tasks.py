import pandas as pd

from app.models import btc_prices
from main import scheduler, db
import yfinance as yf


@scheduler.task("interval", id="grab_prices", days=1, misfire_grace_time=900)
def grab_prices():
    btc_data = yf.download(tickers='BTC-USD', period='1d', interval='1d')
    btc_df = pd.DataFrame(btc_data)
    for index, row in btc_df.iterrows():
        average = (row['High'] + row['Low']) / 2
        formatted_date = str(index).split()[0]
        to_insert = btc_prices(date=formatted_date, open=row['Open'], close=row['Close'], average=average,
                              volume=row['Volume'], high=row['High'], low=row['Low'])
        db.session.add(to_insert)
    db.session.commit()


scheduler.start()
