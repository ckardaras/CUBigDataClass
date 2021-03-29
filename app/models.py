from main import db


class BTC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.DECIMAL)