from flask import render_template
from sqlalchemy import func

from app.models import BTC_Weekly, BTC_Daily, Tweet
from main import app, db


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/chart')
def chart():
    weekly = BTC_Weekly.query.order_by(BTC_Weekly.date).all()
    print(weekly)
    return render_template('chart_example.html', weekly=weekly)


@app.route('/daily/sentiment_chart')
def daily_sentiment_chart():
    #btc_prices = BTC_Daily.query.order_by(BTC_Daily.date).all()
    #tweets = db.session.query(int(func.avg(Tweet.sentiment).label('average')).group_by(Tweet.date).order_by(Tweet.date).all()

    return "te"
    #return render_template('daily/sentiment.html', btc=btc_prices, tweets=tweets)

'''
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)
'''