import pandas as pd
import plotly
import plotly.graph_objects as go

catalog_df = pd.read_csv("catalog_cleaned.csv")

fig = go.Figure(data=[go.Table(
    header=dict(values=list(catalog_df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[catalog_df['entry_uuid'],
                       catalog_df['categories'],
                       catalog_df['entry_date'],
                       catalog_df['entry_date_dt'],
                       catalog_df['entry_text_split'],
                       ],
               fill_color='lavender',
               align='left'))
])

fig.show()

