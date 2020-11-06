import pandas as pd
from datetime import datetime
import uuid


def preprocess_legend():
    legend_df = pd.read_csv("data/raw/legend_scraped_2020-11-05.csv")

    # legend_df['category'] = legend_df['category'].str.strip()
    legend_df['category'] = legend_df['category'].str.replace('–', '')
    legend_df['category'] = legend_df['category'].str.strip()
    legend_df['category_id'] = legend_df.index + 1

    legend_df.to_csv("legend_cleaned.csv", index=False)

    return legend_df


legend_df = preprocess_legend()



catalog_df = pd.read_csv("data/raw/catalogue_scraped_2020-11-05.csv")

for c in catalog_df.columns:
    catalog_df[c] = catalog_df[c].str.strip()

catalog_df[["date_split", "entry_text_split"]] = catalog_df["entry_text"].str.split(" – ", n=1, expand=True)
catalog_df['entry_text_split'] = catalog_df['entry_text_split'].str.strip()


def join_bullet_colors(catalog_row):
    entry_categories_list = []

    legend_bullet_src_list = catalog_row['legend_bullet_src'].strip('][').split(', ')  # TODO: Move this outside the lambda function so it persists
    for b in legend_bullet_src_list:
        b = b.replace("'", "")  # TODO: Move this outside the lambda function so it persists
        category = legend_df[legend_df['img_src'] == b]['category']
        try:
            category_val = category.values[0]
        except:
            category_val = "No Category"
        # category_id = legend_df[legend_df['img_src'] == b]['category_id'].iloc[0]
        print(b)
        print(category_val)
        color = legend_df[legend_df['img_src'] == b]['bullet_color']

        entry_categories_list.append(category_val)

    return entry_categories_list


catalog_df['categories'] = catalog_df.apply(lambda row: join_bullet_colors(row), axis=1)


def reformat_entry_date(catalog_row):
    try:
        # TODO: trim date strings first
        return datetime.strptime(catalog_row['entry_date'], '%B %d, %Y')
    except Exception as e:
        return f"Error ({e}) converting {catalog_row['entry_date']}"


catalog_df['entry_date_dt'] = catalog_df.apply(lambda row: reformat_entry_date(row), axis=1)

catalog_df = catalog_df[['entry_uuid', 'categories', 'entry_date', 'entry_date_dt', 'entry_text_split', 'scrape_timestamp']]

catalog_df.to_csv("catalog_cleaned.csv", index=False)

print(catalog_df['categories'])

# for each element in catalogue_scraped['legend_bullet_src'], match to legend_df['img_src'], return legend_df['category']
# remove date from beginning of string (split on ' – ', then remove columns)
# convert 'entry_date' field to datetime object
