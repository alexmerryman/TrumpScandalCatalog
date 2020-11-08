import pandas as pd
from ast import literal_eval
import datetime
import re
import plotly
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

legend_df = pd.read_csv("data/cleaned/legend_cleaned.csv")
catalog_df = pd.read_csv("data/cleaned/database_cleaned_w_links.csv")

# TODO: Move all of this to processing
def htmlize_links(row):
    str_list = literal_eval(row['entry_links'])

    html_links = []
    for i in str_list:
        i = i.replace(',', '')  # TODO: This doesn't seem to do anything
        link = f"[{i}]({i})\n\n"
        html_links.append(link)

    return html_links


catalog_df['entry_links_markdown'] = catalog_df.apply(lambda row: htmlize_links(row), axis=1)


def markdown_categories(row):
    categories_list = literal_eval(row['categories'])

    categories_markdown = []
    for i in categories_list:
        cat_md = f"{i}\n"
        categories_markdown.append(cat_md)

    return categories_markdown


catalog_df['categories'] = catalog_df.apply(lambda row: markdown_categories(row), axis=1)

catalog_df = catalog_df[~catalog_df['entry_date'].str.contains('Error - unable to extract date')]
catalog_df['entry_date_dt'] = pd.to_datetime(catalog_df['entry_date_dt'], errors='ignore')
catalog_df['entry_date_dt'] = catalog_df['entry_date_dt'].dt.date
catalog_df = catalog_df.sort_values(by='entry_date_dt', ascending=False)  # TODO: Do sorting in another step, save final final df to /raw folder

catalog_df.rename(
    columns={
    'categories': 'Category(s)',
    'entry_date': 'Date',
    'entry_text_split': 'Entry',
    'entry_links_markdown': 'Sources'
    },
    inplace=True)

absolute_min_date = min(catalog_df['entry_date_dt'])
absolute_max_date = datetime.date.today()

categories = legend_df['category'].unique().tolist()
categories.append('-All-')
categories = sorted(categories)


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.YETI]
)
server = app.server


# TODO: Rename columns
# TODO: Dash bootstrap (https://dash-bootstrap-components.opensource.faculty.ai/)
# https://dash.plotly.com/dash-html-components
app.title = 'Every Trump Scandal - Searchable Database'
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-426BZZ2CS2"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-426BZZ2CS2');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(
    children=[
        html.Div(
            id='text-container',
            className='container',
            style={'margin-left': '5px', 'margin-right': '10px'},
            children=[ # TODO: Get this data from scraping
            dcc.Markdown('''
            # Every Trump Scandal
            ## An interactive & searchable database of all of Donald Trump's scandals.
            
            Data sourced from:
            __*[Lest We Forget the Horrors: A Catalog of Trump’s Worst Cruelties, Collusions, Corruptions, and Crimes](https://www.mcsweeneys.net/articles/the-complete-listing-so-far-atrocities-1-967)*__
            
            *by John McMurtrie, Ben Parker, Stephanie Steinbrecher, Kelsey Ronan, Amy Sumerton, Rachel Villa, and Sophia DuRose.*\n
            \------------------------------------\n
            In an effort to improve on the fantastic reporting done by the aforementioned, we scraped the catalog data and made it filterable & searchable here.
            
            Please keep in mind, this is still very much a work in progress, and will be updated as new scandals/reporting emerge.
            Additionally, we am working on extending functionality such as providing enhanced filtering, metrics, and analytics such as frequently-appearing entities and themes.
            
            \------------------------------------\n
            *Database last updated: 11/05/2020 9:35pm EST*
            '''),
            ],
        ),
        html.Div(
            id='filter-container',
            className='container',
            style={'width': '50%', 'margin-left': '5px', 'margin-right': '10px'},
            children=[
            html.H4("Filter by category:"),
            dcc.Dropdown(
                id='filter_dropdown',
                options=[{'label': cat, 'value': cat} for cat in categories],
                # value='-All-',
                multi=True,
                ),
            html.Br(),
            html.H4("Filter by date range:"),
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=absolute_min_date,
                max_date_allowed=absolute_max_date,
                initial_visible_month=absolute_min_date,
                number_of_months_shown=3,
                end_date=absolute_max_date,
                display_format='M/D/Y',
                clearable=True,
            ),
            html.Div(id='output-container-date-picker-range'),
            # TODO: Add date filter
            # TODO: Add common-themes filter (fake news, covid, election, etc)
            # TODO: Make filters independent? Checkbox?
            html.P("Note: You can search catalog entries for specific words or phrases by typing in the field directly below the table header (it is case sensitive)."),
            ],
        ),
        html.Br(),
        html.Div(
            id='datatable-container',
            className='container',
            style={'margin-left': '10px', 'margin-right': '5px'},
            children=[
                dash_table.DataTable(
                    # https://dash.plotly.com/datatable/reference
                    id='table-container',
                    columns=[
                        # {'id': c, 'name': c} for c in catalog_df.columns.values,
                        {'name': 'Category(s)', 'id': 'Category(s)', 'type': 'text', 'presentation': 'markdown'},
                        {'name': 'Date', 'id': 'Date', 'type': 'datetime', 'presentation': 'markdown'},
                        {'name': 'Entry', 'id': 'Entry', 'type': 'text', 'presentation': 'markdown'},
                        {'name': 'Sources', 'id': 'Sources', 'type': 'text', 'presentation': 'markdown'},
                    ],
                    hidden_columns=['entry_uuid', 'entry_date_dt', 'scrape_timestamp'],
                    style_data={
                        'width': '100px',
                        'maxWidth': '100px',
                        'minWidth': '100px',
                    },
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
                    style_cell_conditional=[
                        {'if': {'column_id': 'Sources'},
                         'width': '5px',
                         'overflow': 'hidden',
                         'textOverflow': 'ellipsis',
                         },
                        {'if': {'column_id': 'Category(s)'},
                         'width': '5px'},
                        {'if': {'column_id': 'Date'},
                         'width': '5px'},
                        {'if': {'column_id': 'Entry'},
                         'width': '150px'},
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    filter_action='native',  # TODO: Convert to lowercase, create another column of lower(text) and/or do backend filter with: df[‘column’].contains(‘text’, case=False).
                    page_size=1000,
                    css=[{"selector": ".show-hide", "rule": "display: none"}],
                    # style_table={'display': 'blocl', 'width': '33%', 'margin-left': '0', 'margin-right': '0'},
                ),
            ],
        ),
    ]
)


@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')])
def display_table(cat, start_date, end_date):

    if start_date is None:
        start_date = absolute_min_date

    if end_date is None:
        end_date = datetime.date.today()

    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    # TODO: Do all this date/datetime formatting above
    # print('start date:', start_date, type(start_date))
    # print('end date:', end_date, type(end_date))
    # print('table date:', catalog_df['entry_date_dt'].iloc[3], type(catalog_df['entry_date_dt'].iloc[3]))

    date_filtered_df = catalog_df[(catalog_df['entry_date_dt'] >= start_date) &
                                  (catalog_df['entry_date_dt'] <= end_date)]

    if cat is None:
        cat_filtered_df = date_filtered_df
    elif '-All-' in cat:
        cat_filtered_df = date_filtered_df
    else:
        cat_list_passed_search = [re.escape(c) for c in cat]
        cat_filtered_df = date_filtered_df[date_filtered_df['Category(s)'].str.contains('|'.join(cat_list_passed_search))]
    return cat_filtered_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)