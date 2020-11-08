import pandas as pd
from ast import literal_eval
import datetime


def process_reporting_layer_all():
    legend_df = pd.read_csv("data/cleaned/legend_cleaned.csv")
    catalog_df = pd.read_csv("data/cleaned/database_cleaned_w_links.csv")

    catalog_df = catalog_df[~catalog_df['entry_date'].str.contains('Error - unable to extract date')]
    catalog_df['entry_date_dt'] = pd.to_datetime(catalog_df['entry_date_dt'], errors='ignore')
    catalog_df['entry_date_dt'] = catalog_df['entry_date_dt'].dt.date

    def markdown_links(row):
        str_list = literal_eval(row['entry_links'])
        html_links = "".join([f"- [{i}]({i})\n\n" for i in str_list])

        return html_links

    catalog_df['entry_links_markdown'] = catalog_df.apply(lambda row: markdown_links(row), axis=1)

    categories_emojis = {
        "Sexual Misconduct, Harassment, & Bullying": '🗣',
        "White Supremacy, Racism, Homophobia, Transphobia, & Xenophobia": '🔴',
        "Public Statements / Tweets": '📱',
        "Collusion with Russia & Obstruction of Justice": '⚖',
        "Trump Staff & Administration": '🧑‍💼',
        "Trump Family Business Dealings": '💰',
        "Policy": '📋',
        "Environment": '🏞',
        "No Category": '?',
    }

    def markdown_categories(row):
        categories_list = literal_eval(row['categories'])
        categories_markdown = "".join([f"{categories_emojis[i]} {i}\n\n" for i in categories_list])

        return categories_markdown

    catalog_df['categories'] = catalog_df.apply(lambda row: markdown_categories(row), axis=1)

    catalog_df = catalog_df.sort_values(by='entry_date_dt', ascending=False)  # TODO: Do sorting in another step, save final final df to /raw folder

    categories_for_dropdown_filter = [{"label": "-All-", "value": "-All-"}]

    def category_transform_for_dropdown_filter(row):
        categories_for_dropdown_filter.append({"label": f"{categories_emojis[row['category']]} {row['category']}", "value": row["category_id"]})
        return {row['category']: row['category_id']}

    legend_df['cat_for_dropdown'] = legend_df.apply(lambda row: category_transform_for_dropdown_filter(row), axis=1)

    # TODO: One-hot-encode categories

    def common_themes(df):
        search_themes = {
            "Coronavirus": ["coronavirus", "covid", "mask", "social distance", "social-distance", "social distancing", "social-distancing"],
            "China": ["china", "chinese", "xi jinping", "xi", "jinping"],
            "Russia": ["russia", "russian", "vladimir putin", "vladimir", "putin"],
            "Iran": ["iran", "iranian", "hassan rouhani", "rouhani"],
            "North Korea": ["north korea", "north korean", "kim jong-un", "kim jong un"],
        }

        themes_for_dropdown_filter = [k for k, v in search_themes.items()]

        df["entry_text_lower"] = df["entry_text_split"].str.lower()

        def search_apply_themes(row):
            themes_list = []
            try:
                for k, v in search_themes.items():
                    for term in v:
                        if term in row["entry_text_lower"]:
                            themes_list.append(k)
            except:
                pass

            return list(set(themes_list))

        df["themes"] = df.apply(lambda row: search_apply_themes(row), axis=1)
        return df, themes_for_dropdown_filter

    catalog_df, themes_for_dropdown_filter = common_themes(catalog_df)

    catalog_df.rename(
        columns={
            'categories': 'Category(s)',
            'entry_date': 'Date',
            'entry_text_split': 'Entry',
            'entry_links_markdown': 'Sources'
        },
        inplace=True)

    catalog_df.to_csv('data/reporting_layer/catalog_df_reporting.csv', index=False)
    legend_df.to_csv('data/reporting_layer/legend_df_reporting.csv', index=False)

    return catalog_df, legend_df, categories_for_dropdown_filter, themes_for_dropdown_filter
