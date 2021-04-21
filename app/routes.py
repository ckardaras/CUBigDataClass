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
def btc_daily_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = BTC_Daily.query.filter(BTC_Daily.date >= start, BTC_Daily.date <= end).order_by(BTC_Daily.date).all()
    sentiments = BTC_Sentiments.query.order_by(BTC_Sentiments.date).all()

    chart_title = "BTC Daily Price vs Sentiment"

    return render_template('/bitcoin/sentiment.html', btc=btc_prices, sentiments=sentiments, title=chart_title)


@app.route('/btc/weekly/sentiment')
def btc_weekly_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = BTC_Weekly.query.filter(BTC_Weekly.date >= start, BTC_Weekly.date <= end).order_by(
        BTC_Weekly.date).all()
    sentiments = db.session.execute("""
        select AVG(avg_sentiment)::float, 
            date_trunc('week', date)::date
        from "BTC__sentiments"
        group by 
          date_trunc('week', date)
        order by date_trunc;
    """).fetchall()

    chart_title = "BTC Weekly Price vs Sentiment"

    return render_template('/bitcoin/sentiment.html', btc=btc_prices, sentiments=sentiments, title=chart_title)


@app.route('/btc/monthly/sentiment')
def btc_monthly_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = BTC_Monthly.query.filter(BTC_Monthly.date >= start, BTC_Monthly.date <= end).order_by(
        BTC_Monthly.date).all()
    sentiments = db.session.execute("""
        select AVG(avg_sentiment)::float, 
            date_trunc('month', date)::date
        from "BTC__sentiments"
        group by 
          date_trunc('month', date)
        order by date_trunc;
    """).fetchall()

    chart_title = "BTC Monthly Price vs Sentiment"

    return render_template('/bitcoin/sentiment.html', btc=btc_prices, sentiments=sentiments, title=chart_title)


'''
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)
'''
