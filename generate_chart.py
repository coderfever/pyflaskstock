from io import BytesIO
import urllib.parse
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
import fetch_stock as stk

def combine_stocks(stocks):
    def calc_pct(val):
        return (val - df['Close'][0]) / df['Close'][0] * 100

    num_stocks = len(stocks)
    stock_close_df = pd.DataFrame()
    for key, df in stocks.items():
        print(df['Close'][0])
        stock_close_df[key] = df['Close'].apply(calc_pct)

    stock_close_df.fillna(method='ffill', limit=2, inplace=True)
    # stock_close_df.dropna(inplace=True)
    print(stock_close_df.head())
    return stock_close_df, num_stocks

def generate_plot(stocks):
    stocks_to_plot, num_stocks = combine_stocks(stocks)
    img = BytesIO()
    n = len(stocks[0].index)
    ind = np.arange(n)

    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, n-1)
        return stocks_to_plot.index[thisind].strftime('%Y-%m-%d %H')
    
    fig, ax = plt.subplots(ncols=1)
    for index in range(num_stocks):
        ax.plot(ind, stocks_to_plot['Close{}'.format(index)])

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.show()
    return urllib.parse.quote(base64.b64encode(img.read()).decode())



if __name__ == '__main__':
    F = stk.get_google_finance_intraday(ticker='F', period=60, days=2, exchange='NYSE')
    A = stk.get_google_finance_intraday(ticker='A', period=60, days=2, exchange='NYSE')
    # generate_plot({'F': F, 'A': A})
    combine_stocks({'F': F, 'A': A})