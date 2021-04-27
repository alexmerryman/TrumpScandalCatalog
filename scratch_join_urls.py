import pandas as pd

# catalog_cleaned_df = pd.read_csv('data/cleaned/catalog_cleaned.csv')
# catalog_cleaned_df['entry_text_lower'] = catalog_cleaned_df['entry_text_split'].str.lower()
#
# links_df = pd.read_csv('data/raw/catalogue_scraped_2020-11-05.csv')
#
# for c in links_df.columns:
#     links_df[c] = links_df[c].str.strip()
#
# links_df[["date_split", "entry_text_split"]] = links_df["entry_text"].str.split(" – ", n=1, expand=True)
# links_df['entry_text_split'] = links_df['entry_text_split'].str.strip()
#
# links_df['entry_text_lower_links'] = links_df['entry_text_split'].str.lower()
# links_df = links_df[['entry_text_lower_links', 'entry_links']]
# print(links_df[0:3])
#
# catalog_cleaned_df_joined = pd.merge(left=catalog_cleaned_df, right=links_df,
#                                      how='left',
#                                      left_on='entry_text_lower',
#                                      right_on='entry_text_lower_links',
#                                      )
#
# print(catalog_cleaned_df_joined.columns)
# print(catalog_cleaned_df_joined[['entry_text_lower', 'entry_links']][0:3])
# # print(catalog_cleaned_df_joined[~catalog_cleaned_df_joined['entry_links'].isnull()])
# # print(catalog_cleaned_df_joined['entry_links'].unique().tolist())
# catalog_cleaned_df_joined = catalog_cleaned_df_joined[['entry_uuid', 'entry_links']]
#
# catalog_cleaned_df_final = pd.read_csv('data/cleaned/catalog_cleaned.csv')
# final_merged_df = pd.merge(left=catalog_cleaned_df_final, right=catalog_cleaned_df_joined,
#                            how='left',
#                            on='entry_uuid')
#
# print(final_merged_df.iloc[0])
#
# final_merged_df.to_csv('data/cleaned/database_cleaned_w_links.csv', index=False)




# Join database_cleaned_w_links.csv with legend_cleaned
from ast import literal_eval

database_cleaned_w_links = pd.read_csv('data/cleaned/database_cleaned_w_links.csv')

legend_cleaned_df = pd.read_csv('data/cleaned/legend_cleaned.csv')


def category_ids(row):
    cat_ids_list = []
    for c in literal_eval(row['categories']):
        try:
            cat_id = legend_cleaned_df[legend_cleaned_df['category'] == c]['category_id'].values[0]
        except IndexError:
            cat_id = c
        cat_ids_list.append(cat_id)

    return cat_ids_list


database_cleaned_w_links['category_ids'] = database_cleaned_w_links.apply(lambda row: category_ids(row), axis=1)

print(database_cleaned_w_links['category_ids'])
# database_cleaned_w_links.to_csv('data/cleaned/database_cleaned_w_links.csv', index=False)

test_cats = [2, 1]
# df_contains_cats = database_cleaned_w_links[pd.DataFrame(database_cleaned_w_links['category_ids'].tolist()).isin(test_cats).any(1)]
# print(df_contains_cats['category_ids'])

# df1 = database_cleaned_w_links[database_cleaned_w_links['category_ids'].str.contains('|'.join(test_cats)).any(level=0)]
# print(df1['category_ids'])

mask = database_cleaned_w_links['category_ids'].apply(lambda x: any(item for item in test_cats if item in x))
df1 = database_cleaned_w_links[mask]
print(df1[['categories', 'category_ids']])



