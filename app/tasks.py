import pandas as pd
import re
from datetime import date, datetime
from nltk import RegexpTokenizer, WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
import tweepy as tw
import emot
import nltk
from textblob import TextBlob
from app.models import *
from main import app, db

nltk.download('vader_lexicon') # download vader lexicon
nltk.download("stopwords")
nltk.download("wordnet")

#from app.models import btc_prices
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


@scheduler.task("interval", id="grab_tweets", days=1, misfire_grace_time=900)
def btc_task_grab_sentiment():
    #
    # functions for sentiment analysis
    #
    stop_words = stopwords.words("english")
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    lemmatizer = WordNetLemmatizer()
    tokenzr = RegexpTokenizer('\s+', gaps=True)

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

        o_tweet_text = tweet.text
        tweet_text = convert_emojicon(o_tweet_text)
        tweet_sentiment = TextBlob(tweet_text).sentiment.polarity
        sentiment_counter += tweet_sentiment

        url = f"https://twitter.com/twitter/statuses/{tweet_id}"

        to_insert = btc_tweets(id=tweet_id,
                               date=tweet_time.date(),
                               time=tweet_time.time(),
                               username=tweet_username,
                               hashtags=hashtags,
                               cashtags=cashtags,
                               link=url,
                               sentiment=tweet_sentiment,
                               text=o_tweet_text
                               )
        db.session.add(to_insert)
        if count >= 5000:
            break
        count += 1

    to_insert2 = btc_sentiment(date=datetime.today().strftime('%Y-%m-%d'),
                              avg_sentiment=tweet_sentiment/count
                              )
    db.session.add(to_insert2)
    db.session.commit()
scheduler.start()
