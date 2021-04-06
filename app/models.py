from main import db



class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    tweet = db.Column(db.Text, unique=True)
    sentiment = db.Column(db.Float, nullable=False)

class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    bitcoin_avg_price = db.Column(db.Float, nullable=False)
    bitcoin_day_high = db.Column(db.Float, nullable=False)
    bitcoin_day_low = db.Column(db.Float, nullable=False)
    ethereum_avg_price = db.Column(db.Float, nullable=False)
    ethereum_day_high = db.Column(db.Float, nullable=False)
    ethereum_day_low = db.Column(db.Float, nullable=False)

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    week_id = db.Column(db.Integer)
    month_id = db.Column(db.Integer)

class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month_btc_avg = db.Column(db.Float, nullable=False)
    month_btc_high = db.Column(db.Float, nullable=False)
    month_btc_low = db.Column(db.Float, nullable=False)
    month_btc_sent_avg = db.Column(db.Float, nullable=False)
    month_eth_avg = db.Column(db.Float, nullable=False)
    month_eth_high = db.Column(db.Float, nullable=False)
    month_eth_low = db.Column(db.Float, nullable=False)
    month_eth_sent_avg = db.Column(db.Float, nullable=False)

class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_btc_avg = db.Column(db.Float, nullable=False)
    week_btc_high = db.Column(db.Float, nullable=False)
    week_btc_low = db.Column(db.Float, nullable=False)
    week_btc_sent_avg = db.Column(db.Float, nullable=False)
    week_eth_avg = db.Column(db.Float, nullable=False)
    week_eth_high = db.Column(db.Float, nullable=False)
    week_eth_low = db.Column(db.Float, nullable=False)
    week_eth_sent_avg = db.Column(db.Float, nullable=False)


