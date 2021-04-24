from main import db


class BTC_Tweet(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    username = db.Column(db.Text)
    hashtags = db.Column(db.Text)
    cashtags = db.Column(db.Text)
    link = db.Column(db.Text)
    sentiment = db.Column(db.Float, nullable=False)
    text = db.Column(db.Text)

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



class BTC_Sentiments(db.Model):
    date = db.Column(db.Date, primary_key=True)
    avg_sentiment = db.Column(db.DECIMAL)

class ETH_Sentiments(db.Model):
    date = db.Column(db.Date, primary_key=True)
    avg_sentiment = db.Column(db.DECIMAL)

class BTC_Daily(db.Model):
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.DECIMAL)
    high = db.Column(db.DECIMAL)
    low = db.Column(db.DECIMAL)
    close = db.Column(db.DECIMAL)
    average = db.Column(db.DECIMAL)
    volume = db.Column(db.DECIMAL)


class ETH_Daily(db.Model):
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.DECIMAL)
    high = db.Column(db.DECIMAL)
    low = db.Column(db.DECIMAL)
    close = db.Column(db.DECIMAL)
    average = db.Column(db.DECIMAL)
    volume = db.Column(db.DECIMAL)


class BTC_Weekly(db.Model):
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


class BTC_Monthly(db.Model):
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