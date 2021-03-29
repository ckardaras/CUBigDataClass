from flask import render_template

from app.models import BTC
from main import app, db


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/query')
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)