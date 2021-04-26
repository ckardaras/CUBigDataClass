import math
import random
from datetime import date

from flask import render_template, send_file, request
from sqlalchemy import func

from app.models import *
from main import app, db


@app.route('/')
@app.route('/dashboard')
def dashboard():
    price = btc_prices.query.order_by(btc_prices.date).all()
    return render_template('dashboard.html', prices=price)


@app.route('/btc/news')
def btc_news():
    since = request.args.get('since')
    news_articles = None
    if since is None:
        news_articles = btc_articles.query.order_by(func.random()).limit(30).all()
    else:
        news_articles = btc_articles.query.filter(btc_articles.date >= since).order_by(func.random()).limit(30).all()

    return render_template('bitcoin/news.html', articles=news_articles)


@app.route('/btc/tweets')
def btc_dashboard_tweets():
    since = request.args.get('since')
    tweets = None

    if since is None:
        count = 2772897
        random_row = math.floor(random.uniform(0, 1) * count)
        tweets = btc_tweets.query.offset(random_row).limit(30).all()
    else:
        tweets = btc_tweets.query.filter(btc_tweets.date >= since).order_by(func.random()).limit(30).all()

    return render_template('bitcoin/tweets.html', tweets=tweets)


@app.route('/btc/cards')
def btc_cards():
    tweet_count = 6
    price_count = btc_prices.query.count()
    news_count = btc_articles.query.count()
    return render_template('bitcoin/cards.html', tweet_count=tweet_count, price_count=price_count,
                           news_count=news_count)


@app.route('/btc/price')
def btc_daily_price():
    price = btc_prices.query.order_by(btc_prices.date).all()
    chart_title = "BTC Daily Price"
    return render_template('/bitcoin/price.html', prices=price, title=chart_title)


@app.route('/btc/sentiment')
def btc_daily_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=4, day=24)
    prices = btc_prices.query.filter(btc_prices.date >= start, btc_prices.date <= end).order_by(btc_prices.date).all()
    tweet_sentiments = btc_sentiments.query.filter(btc_sentiments.date >= start, btc_sentiments.date <= end).order_by(btc_sentiments.date).all()
    article_sentiment = btc_article_sentiments.query.filter(btc_article_sentiments.date >= start, btc_article_sentiments.date <= end).order_by( btc_article_sentiments.date).all()

    chart_title = "BTC Daily Price vs Sentiment"

    return render_template('/bitcoin/sentiment.html', btc=prices, tweet_sentiments=tweet_sentiments, article_sentiments=article_sentiment, title=chart_title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.route('/wordcloud')
def d3_wordcloud():
    return render_template('/wordcloud.html', title='word cloud')


@app.route('/eth/daily/price')
def eth_daily_price():
    price = ETH_Daily.query.order_by(ETH_Daily.date).all()
    chart_title = "ETH Daily Price"
    return render_template('/ethereum/price.html', prices=price, title=chart_title)


@app.route('/eth/weekly/price')
def eth_weekly_price():
    price = ETH_Weekly.query.order_by(ETH_Weekly.date).all()
    chart_title = "ETH Weekly Price"
    return render_template('/ethereum/price.html', prices=price, title=chart_title)


@app.route('/eth/monthly/price')
def eth_monthly_price():
    price = ETH_Monthly.query.order_by(ETH_Monthly.date).all()
    chart_title = "ETH Monthly Price"
    return render_template('/ethereum/price.html', prices=price, title=chart_title)


@app.route('/eth/daily/sentiment')
def eth_daily_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = ETH_Daily.query.filter(ETH_Daily.date >= start, ETH_Daily.date <= end).order_by(ETH_Daily.date).all()
    sentiments = ETH_Sentiments.query.order_by(ETH_Sentiments.date).all()

    chart_title = "ETH Daily Price vs Sentiment"

    print(sentiments)

    return render_template('/ethereum/sentiment.html', btc=btc_prices, sentiments=sentiments, title=chart_title)


@app.route('/eth/weekly/sentiment')
def eth_weekly_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = ETH_Weekly.query.filter(ETH_Weekly.date >= start, ETH_Weekly.date <= end).order_by(
        ETH_Weekly.date).all()
    sentiments = db.session.execute("""
        select AVG(avg_sentiment)::float, 
            date_trunc('week', date)::date
        from "ETH__sentiments"
        group by 
          date_trunc('week', date)
        order by date_trunc;
    """).fetchall()

    chart_title = "ETH Weekly Price vs Sentiment"

    return render_template('/ethereum/sentiment.html', btc=btc_prices, sentiments=sentiments, title=chart_title)


@app.route('/eth/monthly/sentiment')
def eth_monthly_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    btc_prices = ETH_Monthly.query.filter(ETH_Monthly.date >= start, ETH_Monthly.date <= end).order_by(
        ETH_Monthly.date).all()
    sentiments = db.session.execute("""
        select AVG(avg_sentiment)::float, 
            date_trunc('month', date)::date
        from "ETH__sentiments"
        group by 
          date_trunc('month', date)
        order by date_trunc;
    """).fetchall()

    chart_title = "ETH Monthly Price vs Sentiment"

    return render_template('/ethereum/sentiment.html', btc=btc_prices, sentiments=sentiments, title=chart_title)


'''
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)
'''
