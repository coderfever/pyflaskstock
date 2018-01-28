from flask import Flask, render_template, request, abort
import pandas as pd

import fetch_stock as stk
import generate_chart as gc

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_homepage():
    ticker = 'F'
    stock = stk.get_google_finance_intraday(ticker='F', period=60, days=5, exchange='NYSE')
    plot_url = gc.generate_plot(stock)
    return render_template('home.html', plot_url=plot_url, ticker=ticker)

@app.route('/', methods=['POST'])
def create_stock_chart():
    ticker = str(request.form['symbol'])
    period = request.form['freq']
    stock = stk.get_google_finance_intraday(ticker=ticker.upper(), period=period, days=5, exchange='NYSE')
    plot_url = gc.generate_plot(stock)
    return render_template('home.html', plot_url=plot_url, ticker=ticker)


if __name__ == '__main__':
    app.run(debug=True)
