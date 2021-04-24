from datetime import date, datetime

from flask import render_template, send_file
from nltk import RegexpTokenizer, WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
from sqlalchemy import func


from app.models import *
from main import app, db


@app.route('/')
def home():
    return render_template('dashboard.html')


@app.route('/btc/price')
def btc_daily_price():
    price = btc_prices.query.order_by(btc_prices.date).all()
    chart_title = "BTC Daily Price"
    return render_template('/bitcoin/price.html', prices=price, title=chart_title)


@app.route('/btc/sentiment')
def btc_daily_sentiment():
    start = date(year=2020, month=3, day=21)
    end = date(year=2021, month=3, day=16)
    prices = btc_prices.query.filter(btc_prices.date >= start, btc_prices.date <= end).order_by(btc_prices.date).all()
    sentiments = BTC_Sentiments.query.order_by(BTC_Sentiments.date).all()

    chart_title = "BTC Daily Price vs Sentiment"

    return render_template('/bitcoin/sentiment.html', btc=prices, sentiments=sentiments, title=chart_title)


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


@app.route('/btc/dailyschedule')
def btc_task_grab_sentiment():
    #
    # functions for sentiment analysis
    #
    def stem_tokenize(text):
        tokenized_text = tokenzr.tokenize(text.lower())
        words = [lemmatizer.lemmatize(w) for w in tokenized_text if w not in stop_words]
        stem_text = " ".join([stemmer.stem(i) for i in words])
        return stem_text  # converted emoji to unicode description of emoji is return as string text


    def regex_tweet(tweet):
        tweet = ' '.join(re.sub("(\$[A-Za-z0-9]+)", " ", tweet).split())
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())
        tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
        tweet = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet).split())
        tweet = ' '.join(re.sub("[\[\]]", " ", tweet).split())
        return tweet


    def clean_mean(val):
        return val.replace('_', ' ').replace('-', ' ').replace(':', ' ')


    def convert_emojicon(text):
        for emoti in emot.emo_unicode.EMOTICONS:
            if emoti in text:
                text = text.replace(emoti, clean_mean(emot.emo_unicode.EMOTICONS.get(emoti, '')))

        for emoti in emot.emo_unicode.UNICODE_EMO:
            if emoti in text:
                text = text.replace(emoti, clean_mean(emot.emo_unicode.UNICODE_EMO.get(emoti, '')))

        for emoti in emot.emo_unicode.EMOTICONS_EMO:
            if emoti in text:
                text = text.replace(emoti, clean_mean(emot.emo_unicode.EMOTICONS_EMO.get(emoti, '')))

        return text
    #
    #
    # Grab tweets
    ##### Tokens
    consumer_key = 'Ou9XaMR4qgy3KGr7cSfvhjnYl'
    consumer_secret = 'kTl5Vs6918QYgEkufJVPbpfbuyFAyyjYfkRcl2hAL5BjGyqxyj'
    access_token = '2991366318-LhMbjkJGvNkmO5bwSzVfMhZQWl19dzoPdgOWD8V'
    access_token_secret = 'qmRpWmw2UHP3VPYOoodeOIt2s8liaGnEaePDSF9JtFIYI'
    ### Connect to API
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    ### Set search words (default is bitcoin)
    search_words = "#btc OR #bitcoin OR bitcoin OR btc"
    ### Set time (Daily)
    date_since = datetime.today().strftime('%Y-%m-%d')
    ### Tweet object
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       since=date_since).items()
    stop_words = stopwords.words("english")
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    lemmatizer = WordNetLemmatizer()
    tokenzr = RegexpTokenizer('\s+', gaps=True)



    sia = SIA()

    count = 0
    sentiment_counter = 0
    for tweet in tweets:
        tweet_id = tweet.id
        tweet_time = tweet.created_at
        tweet_username = tweet.author.screen_name

        tweet_hashtags = tweet.entities['hashtags']
        hashtags = []
        for hashtag in tweet_hashtags:
            hashtags.append(hashtag['text'])

        cashtags = ""
        link = "https://twitter.com/{username}/status/{id}".format(username=tweet_username, id=tweet_id)

        tweet_text = tweet.text
        tweet_text = convert_emojicon(tweet_text)

        tweet_sentiment = TextBlob(tweet_text).sentiment.polarity
        sentiment_counter += tweet_sentiment

        print(tweet_id, tweet_date, tweet_username, hashtags, link, tweet_text, tweet_sentiment)
        count += 1
        if count > 5:
            break