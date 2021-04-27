import math
import random
from datetime import date

from flask import render_template, send_file, request
from sqlalchemy import func

from app.models import *
from main import app, db
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from datetime import date
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt

@app.route('/')
@app.route('/dashboard')
def dashboard():
    tweet_count = 2920503
    price_count = btc_prices.query.count()
    news_count = btc_articles.query.count()
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=4, day=24)
    prices = btc_prices.query.filter(btc_prices.date >= start, btc_prices.date <= end).order_by(btc_prices.date).all()
    tweet_sentiments = btc_sentiments.query.filter(btc_sentiments.date >= start, btc_sentiments.date <= end).order_by(
        btc_sentiments.date).all()
    article_sentiment = btc_article_sentiments.query.filter(btc_article_sentiments.date >= start,
                                                            btc_article_sentiments.date <= end).order_by(
        btc_article_sentiments.date).all()
    return render_template('dashboard.html', prices=prices, tweet_sentiments=tweet_sentiments, article_sentiments=article_sentiment, tweet_count=tweet_count, price_count=price_count,
                           news_count=news_count)

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

    return render_template('/bitcoin/sentiment.html', btc=prices, tweet_sentiments=tweet_sentiments,
                           article_sentiments=article_sentiment, title=chart_title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.route('/wordcloud')
def wordcloud():
    credentials = "postgresql://postgres:Dev12345!@54.165.83.41:5432/tothemoon"
    subtract_byMonths = 0
    startdate = (date(year=2021, month=4, day=24)+relativedelta(months=-subtract_byMonths))
    enddate = date(year=2021, month=4, day=24)

    sql_btc = """SELECT text,date 
                FROM public.btc_tweets
                WHERE public.btc_tweets.date BETWEEN %s AND %s
                """
    df_btc = pd.read_sql(sql_btc, con = credentials,params=[startdate, enddate])
    df_btc = df_btc.dropna(inplace=False)
    text_btc = " ".join(review for review in df_btc.text)
    # print ("There are {} words in the combination of all review.".format(len(text)))
    stopwords = set(STOPWORDS)
    wordcl_btc = WordCloud(stopwords=stopwords, background_color="black", max_font_size=300, max_words=1000, width=1000, height=600).generate(text_btc)
    wordcl_btc.to_file("./static/img/wordcloud_btc.png")

    sql_eth = """SELECT text,date 
                FROM public."ETH__tweet"
                WHERE public."ETH__tweet".date BETWEEN %s AND %s
                """
    df_eth = pd.read_sql(sql_eth, con = credentials,params=[startdate, enddate])
    df_eth = df_eth.dropna(inplace=False)
    text_eth = " ".join(review for review in df_eth.text)
    # print ("There are {} words in the combination of all review.".format(len(text)))
    wordcl_eth = WordCloud(stopwords=stopwords, background_color="black", max_font_size=200, max_words=500, width=1000, height=600).generate(text_eth)
    # saving as image
    wordcl_eth.to_file("./static/img/wordcloud_eth.png")
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
    sentiments = ETH_Sentiments.query.filter(ETH_Daily.date >= start, ETH_Daily.date <= end).order_by(ETH_Sentiments.date).all()

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


@app.route('/eth/tweets')
def eth_dashboard_tweets():
    since = request.args.get('since')
    tweets = None

    if since is None:
        count = 17216
        random_row = math.floor(random.uniform(0, 1) * count)
        tweets = ETH_Tweet.query.offset(random_row).limit(30).all()
    else:
        tweets = ETH_Tweet.query.filter(ETH_Tweet.date >= since).order_by(func.random()).limit(30).all()


    return render_template('ethereum/tweets.html', tweets=tweets)

@app.route('/eth/news')
def eth_news():
    since = request.args.get('since')
    news_articles = None
    if since is None:
        news_articles = eth_articles.query.order_by(func.random()).limit(30).all()
    else:
        news_articles = eth_articles.query.filter(eth_articles.date >= since).order_by(func.random()).limit(30).all()

    return render_template('ethereum/news.html', articles=news_articles)

@app.route('/eth/cards')
def eth_cards():
    tweet_count = 6
    price_count = eth_prices.query.count()
    news_count = eth_articles.query.count()
    return render_template('ethereum/cards.html', tweet_count=tweet_count, price_count=price_count,
                           news_count=news_count)
@app.route('/eth/dashboard')
def eth_dashboard():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=4, day=24)
    prices = eth_prices.query.filter(eth_prices.date >= start, eth_prices.date <= end).order_by(eth_prices.date).all()
    tweet_sentiments = ETH_Sentiments.query.filter(ETH_Sentiments.date >= start, ETH_Sentiments.date <= end).order_by(
        ETH_Sentiments.date).all()
    article_sentiment = eth_article_sentiments.query.filter(eth_article_sentiments.date >= start,
                                                            eth_article_sentiments.date <= end).order_by(
        eth_article_sentiments.date).all()
    return render_template('ethereum/dashboard.html', prices=prices, tweet_sentiments=tweet_sentiments, article_sentiments=article_sentiment)
'''
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)
'''
