import plotly.offline as pto
import plotly.graph_objs as go
import numpy as np

def gen_plotly():
    N = 1000
    random_x = np.random.randn(N)
    random_y = np.random.randn(N)

    # Create a trace
    trace = go.Scatter(
        x = random_x,
        y = random_y,
        mode = 'markers'
    )

    data = [trace]
    layout = go.Layout(title='Test', xaxis=dict(title='Months'), yaxis=dict(title='Test'))

    # Plot and embed in ipython notebook!
    fig = go.Figure(data=data, layout=layout)
    div_output = pto.plot(fig, output_type="div", include_plotlyjs=False)
    return div_output
