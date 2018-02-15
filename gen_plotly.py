import plotly.offline as pto
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import fetch_stock as stk

def combine_stocks(stocks):
    '''
    Combine multiple stocks into a single DataFrame
    Input: stock dataframes as a dict
    Output: DF of percent change for each stock,
    '''
    def calc_pct(val):
        return (val - df['Close'][0]) / df['Close'][0] * 100

    stock_close_df = pd.DataFrame()

    for key, df in stocks.items():
        stock_close_df[key] = df['Close'].apply(calc_pct)
        
    stock_close_df.fillna(method='ffill', limit=2, inplace=True)

    correlation = stock_close_df.corr().to_html()

    return stock_close_df, correlation

def gen_compare_plots(stocks):
    stocks_to_plot, correlation = combine_stocks(stocks)
    print(stocks_to_plot.head())
    n = len(stocks_to_plot.index)
    ind = np.arange(len(stocks_to_plot.index))
    
    data = list()
    for symbol in stocks.keys():
        trace = go.Scatter(
            x = ind,
            y = stocks_to_plot[symbol],
            name = symbol
        )
        data.append(trace)

    tickvals = [stocks_to_plot.index.strftime('%Y-%m-%d').tolist().index(x) 
                for x in np.unique(stocks_to_plot.index.strftime('%Y-%m-%d'))]
    ticktext= stocks_to_plot.index[tickvals].strftime('%Y-%m-%d %H:%M')
    print(ticktext)
    print(tickvals, stocks_to_plot.index[tickvals] )

    layout = go.Layout(
        title='Compare', 
        xaxis=dict(
            title = 'Date', 
            ticktext = ticktext,
            tickvals = tickvals
            ), 
        yaxis=dict(title='Pct Change')
    )

    fig = go.Figure(data=data, layout=layout)
    div_output = pto.plot(fig, output_type="div", include_plotlyjs=False)
    return div_output, correlation


def gen_plotly():
    N = 100
    
    data = list()
    # Create a trace
    for _ in range(2):
        random_x = [x for x in range(N)]
        random_y = np.random.randn(N)
        trace = go.Scatter(
            x = random_x,
            y = random_y,
        )
        data.append(trace)
    layout = go.Layout(title='Test', xaxis=dict(title='Months'), yaxis=dict(title='Test'))

    # Plot and embed in ipython notebook!
    fig = go.Figure(data=data, layout=layout)
    div_output = pto.plot(fig, output_type="div", include_plotlyjs=False)
    return div_output

if __name__ == '__main__':
    F = stk.get_google_finance_intraday(ticker='F', period=60, days=5, exchange='NYSE')
    A = stk.get_google_finance_intraday(ticker='A', period=60, days=5, exchange='NYSE')
    gen_compare_plots({'F':F, 'A': A})
