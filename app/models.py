from main import db


class btc_tweets(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    username = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    cashtags = db.Column(db.Text)
    link = db.Column(db.Text)
    sentiment = db.Column(db.Float, nullable=False)
    text = db.Column(db.Text)


class btc_sentiments(db.Model):
    date = db.Column(db.Date, primary_key=True)
    avg_sentiment = db.Column(db.DECIMAL)


class btc_article_sentiments(db.Model):
    date = db.Column(db.Date, primary_key=True)
    avg_sentiment = db.Column(db.DECIMAL)


class btc_prices(db.Model):
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.DECIMAL)
    high = db.Column(db.DECIMAL)
    low = db.Column(db.DECIMAL)
    close = db.Column(db.DECIMAL)
    average = db.Column(db.DECIMAL)
    volume = db.Column(db.DECIMAL)


class btc_articles(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    article_url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    headline = db.Column(db.Text)
    date = db.Column(db.Date)
    sentiment = db.Column(db.Integer)  # -1 = Negative, 0 = Neutral, 1 = Positive


class ETH_Sentiments(db.Model):
    date = db.Column(db.Date, primary_key=True)
    avg_sentiment = db.Column(db.DECIMAL)


class ETH_Tweet(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    username = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    cashtags = db.Column(db.Text)
    link = db.Column(db.Text)
    sentiment = db.Column(db.Float, nullable=False)
    text = db.Column(db.Text)


class ETH_Daily(db.Model):
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.DECIMAL)
    high = db.Column(db.DECIMAL)
    low = db.Column(db.DECIMAL)
    close = db.Column(db.DECIMAL)
    average = db.Column(db.DECIMAL)
    volume = db.Column(db.DECIMAL)


class ETH_Weekly(db.Model):
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.DECIMAL)
    high = db.Column(db.DECIMAL)
    low = db.Column(db.DECIMAL)
    close = db.Column(db.DECIMAL)
    average = db.Column(db.DECIMAL)
    volume = db.Column(db.DECIMAL)


class ETH_Monthly(db.Model):
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.DECIMAL)
    high = db.Column(db.DECIMAL)
    low = db.Column(db.DECIMAL)
    close = db.Column(db.DECIMAL)
    average = db.Column(db.DECIMAL)
    volume = db.Column(db.DECIMAL)
