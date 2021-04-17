from flask import render_template

from app.models import BTC_Weekly
from main import app
import pandas as pd

@app.route('/')
def home():
    df = pd.read_csv('data.csv')
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}

    return render_template('home.html')


@app.route('/chart')
def chart():
    weekly = BTC_Weekly.query.order_by(BTC_Weekly.date).all()
    print(weekly)
    return render_template('chart_example.html', weekly=weekly)



'''
def query():
    new_row = BTC(price=5.3)
    db.session.add(new_row)
    db.session.commit()
    row = BTC.query.filter(BTC.id == 1).first()
    return render_template('query.html', row=row)
'''