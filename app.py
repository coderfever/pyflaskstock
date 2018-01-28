import fetch_stock as stk
from flask import Flask, render_template, request, abort
import pandas as pd

import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import urllib.parse

app = Flask(__name__)

def generate_plot(stock):
    img = BytesIO()
    y = stock.Close
    x = stock.index
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)
    return urllib.parse.quote(base64.b64encode(img.read()).decode())

@app.route('/', methods=['GET'])
def get_homepage():
    stock = stk.get_google_finance_intraday(ticker='F', period=60, days=5, exchange='NYSE')
    plot_url = generate_plot(stock)
    return render_template('home.html', plot_url=plot_url)

@app.route('/', methods=['POST'])
def create_stock_chart():
    # if request.form:
    ticker = str(request.form['symbol'])
    period = request.form['freq']
    # if not request.form or not 'symbol' in request.form:
    #     abort(400)

    stock = stk.get_google_finance_intraday(ticker=ticker.upper(), period=period, days=5, exchange='NYSE')

    # return stock.to_html()
    plot_url = generate_plot(stock)
    return render_template('home.html', plot_url=plot_url)
    # return period
    # if request.method == 'POST':
    #   result = request.form['Physics']
    #   return render_template("home.html",result = result)

if __name__ == '__main__':
    app.run(debug=True)
