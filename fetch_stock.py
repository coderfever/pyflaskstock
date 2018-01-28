# http://dacatay.com/data-science/download-free-intraday-stock-data-from-google-finance-with-python/#more-1548

import csv
import datetime
import re
import codecs
import requests
import pandas as pd
# import cufflinks as cf
# from plotly.offline import init_notebook_mode, iplot

def get_google_finance_intraday(ticker, period=60, days=1, exchange='NASD'):
    """
    Retrieve intraday stock data from Google Finance.
    
    Parameters
    ----------------
    ticker : str
        Company ticker symbol.
    period : int
        Interval between stock values in seconds.
        i = 60 corresponds to one minute tick data
        i = 86400 corresponds to daily data
    days : int
        Number of days of data to retrieve.
    exchange : str
        Exchange from which the quotes should be fetched
    
    Returns
    ---------------
    df : pandas.DataFrame
        DataFrame containing the opening price, high price, low price,
        closing price, and volume. The index contains the times associated with
        the retrieved price values.
    """
    # build url
    url = 'https://finance.google.com/finance/getprices'+\
            '?p={days}d&f=d,o,h,l,c,v&q={ticker}&i={period}&x={exchange}'.format(ticker=ticker,
                                                                                period=period,
                                                                                days=days,
                                                                                exchange=exchange)
    page = requests.get(url)
    reader = csv.reader(codecs.iterdecode(page.content.splitlines(),"utf-8"))
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    rows=[]
    times=[]

    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start+datetime.timedelta(seconds=int(period) * int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'), columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date'))

if __name__ == '__main__':
    F = get_google_finance_intraday(ticker='F', period=60, days=2, exchange='NYSE')
    print(F.head())