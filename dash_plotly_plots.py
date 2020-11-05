import pandas as pd
import plotly
import plotly.graph_objects as go

catalog_df = pd.read_csv("catalog_cleaned.csv")

fig = go.Figure(data=[go.Table(
    header=dict(values=['Entry UUID', 'Categories', 'Entry Date', 'Entry'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[catalog_df['entry_uuid'],
                       catalog_df['categories'],
                       # catalog_df['entry_date'],
                       catalog_df['entry_date_dt'],
                       catalog_df['entry_text_split'],
                       ],
               fill_color='lavender',
               align='left'))
])


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)
