from datetime import date

from flask import render_template
from sqlalchemy import func

from app.models import BTC_Weekly, BTC_Daily, Tweet, BTC_Sentiments, BTC_Monthly
from main import app, db


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/btc/daily/price')
def btc_daily_price():
    price = BTC_Daily.query.order_by(BTC_Daily.date).all()
    chart_title = "BTC Daily Price"
    return render_template('/bitcoin/price.html', prices=price, title=chart_title)


@app.route('/btc/weekly/price')
def btc_weekly_price():
    price = BTC_Weekly.query.order_by(BTC_Weekly.date).all()
    chart_title = "BTC Weekly Price"
    return render_template('/bitcoin/price.html', prices=price, title=chart_title)


@app.route('/btc/monthly/price')
def btc_monthly_price():
    price = BTC_Monthly.query.order_by(BTC_Monthly.date).all()
    chart_title = "BTC Monthly Price"
    return render_template('/bitcoin/price.html', prices=price, title=chart_title)


@app.route('/btc/daily/sentiment')
def daily_sentiment_chart():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = BTC_Daily.query.filter(BTC_Daily.date >= start, BTC_Daily.date <= end).order_by(BTC_Daily.date).all()
    sentiments = BTC_Sentiments.query.order_by(BTC_Sentiments.date).all()
    print("lol", sentiments)

    return render_template('/bitcoin/daily/sentiment.html', btc=btc_prices, sentiments=sentiments)

'''
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)
'''