import pandas as pd
import plotly
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html

legend_df = pd.read_csv("data/cleaned/legend_cleaned.csv")
catalog_df = pd.read_csv("data/cleaned/catalog_cleaned.csv")
catalog_df = catalog_df.sort_values(by='entry_date_dt', ascending=False)  # TODO: Do sorting in another step, save final final df to /raw folder

categories = legend_df['category'].unique().tolist()
categories.append('-All-')
categories = sorted(categories)


app = dash.Dash(__name__)
server = app.server


# TODO: Rename columns
# TODO: Dash bootstrap (https://dash-bootstrap-components.opensource.faculty.ai/)
# https://dash.plotly.com/dash-html-components

app.title = 'Trump Scandal Catalog'

app.layout = html.Div(
    children=[
        html.Div(children=[ # TODO: Get this data from scraping
            html.H1(""),
            html.H2(""),
            html.I(""),
            dcc.Markdown('''
            # Every Trump Scandal
            ## An interactive and searchable database of all of Donald Trump's scandals.
            A project by Alex Merryman ([GitHub repo](https://github.com/alexmerryman/TrumpScandalCatalog))
            
            Data sourced from:
            
            __*[Lest We Forget the Horrors: A Catalog of Trump’s Worst Cruelties, Collusions, Corruptions, and Crimes](https://www.mcsweeneys.net/articles/the-complete-listing-so-far-atrocities-1-967)*__
            
            *by John McMurtrie, Ben Parker, Stephanie Steinbrecher, Kelsey Ronan, Amy Sumerton, Rachel Villa, and Sophia DuRose.*\n
            \------------\n
            In an effort to improve on the fantastic reporting done by the aforementioned, I scraped the catalog data and made it filterable & searchable here.
            
            Please keep in mind, this is still very much a work in progress, and will be updated as new scandals/reporting emerge.
            Additionally, I am working on extending functionality such as providing enhanced filtering, metrics, and analytics such as frequently-appearing entities and themes.
            '''),
            ],
        ),
        html.Div(children=[
            html.H4("Filter by category:"),
            dcc.Dropdown(
                id='filter_dropdown',
                options=[{'label': cat, 'value': cat} for cat in categories],
                value='-All-',
                ),
            # TODO: Add date filter
            # TODO: Add common-themes filter (fake news, covid, election, etc)
            # TODO: Make filters independent? Checkbox?
            html.P("Note: You can search catalog entries for specific words or phrases by typing in the field directly below the table header (it is case sensitive)."),
            ],
            style={'width': '30%'},
        ),
        # html.Div(children=[
        #     html.H4("Categories:"),
        #     html.Ul(children=[
        #         html.Li(
        #             html.Area(
        #                 style={
        #                     'shape': 'circle',
        #                     # 'height': '25px',
        #                     # 'width': '25px',
        #                     # 'background_color': '#ff5733',
        #                     # 'border_radius': '50%',
        #                     # 'display': 'inline-block',
        #                 }
        #             )
        #         ),
        #     ]),
        # ]),
        html.Br(),
        dash_table.DataTable(
            # https://dash.plotly.com/datatable/reference
            id='table-container',
            columns=[{'id': c, 'name': c} for c in catalog_df.columns.values],
            hidden_columns=['entry_uuid', 'scrape_timestamp'],
            style_cell={
                'font_family': 'helvetica',
                'font_size': '12px',
                'whiteSpace': 'normal',
                # 'height': 'auto',
                # 'lineHeight': '15px',
                'textAlign': 'left',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            filter_action='native',  # TODO: Convert to lowercase, create another column of lower(text) and/or do backend filter with: df[‘column’].contains(‘text’, case=False).
            page_size=1000,
        )
    ]
)


@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value')])
def display_table(cat):
    if cat == '-All-' or cat is None:
        dff = catalog_df
    else:
        dff = catalog_df[catalog_df['categories'].str.contains(cat)]
    return dff.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)