from flask import Flask, render_template, request, abort, Markup
import pandas as pd

import fetch_stock as stk
import generate_chart as gc
import gen_plotly as gp

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_homepage():
    ticker = 'F'
    stock = stk.get_google_finance_intraday(ticker='F', period=60, days=5, exchange='NYSE')
    plot_url = gc.generate_plot(stock)
    return render_template('home.html', plot_url=plot_url, ticker=ticker)

@app.route('/', methods=['POST'])
def create_stock_chart():
    ticker = str(request.form['ticker']).upper()
    print(ticker)
    period = 60#request.form['freq']
    stock = stk.get_google_finance_intraday(ticker=ticker, period=period, days=5, exchange='NYSE')
    plot_url = gc.generate_plot(stock)
    return render_template('home.html', plot_url=plot_url, ticker=ticker)

@app.route('/plotly', methods=['GET'])
def test_plotly():
    div = gp.gen_plotly()
    return render_template('test.html', plotly=Markup(div))

if __name__ == '__main__':
    app.run(debug=True)
