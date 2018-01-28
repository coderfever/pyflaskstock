from io import BytesIO
import urllib.parse
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
import fetch_stock as stk


def generate_plot(stock):
    img = BytesIO()
    n = len(stock.index)
    ind = np.arange(n)

    def format_date(x, pos=None):
        thisind = np.clip(int(x + 0.5), 0, n-1)
        return stock.index[thisind].strftime('%Y-%m-%d %H')
    
    fig, ax = plt.subplots(ncols=1)

    ax.plot(ind, stock.Close)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    fig.autofmt_xdate()
    fig.savefig(img, format='png')
    img.seek(0)
    return urllib.parse.quote(base64.b64encode(img.read()).decode())

if __name__ == '__main__':
    F = stk.get_google_finance_intraday(ticker='F', period=60, days=2, exchange='NYSE')
    generate_plot(F)