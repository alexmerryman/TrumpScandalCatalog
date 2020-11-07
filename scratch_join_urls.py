import pandas as pd

catalog_cleaned_df = pd.read_csv('data/cleaned/catalog_cleaned.csv')
catalog_cleaned_df['entry_text_lower'] = catalog_cleaned_df['entry_text_split'].str.lower()



links_df = pd.read_csv('data/raw/catalogue_scraped_2020-11-05.csv')

for c in links_df.columns:
    links_df[c] = links_df[c].str.strip()

links_df[["date_split", "entry_text_split"]] = links_df["entry_text"].str.split(" – ", n=1, expand=True)
links_df['entry_text_split'] = links_df['entry_text_split'].str.strip()

links_df['entry_text_lower_links'] = links_df['entry_text_split'].str.lower()
links_df = links_df[['entry_text_lower_links', 'entry_links']]
print(links_df[0:3])

catalog_cleaned_df_joined = pd.merge(left=catalog_cleaned_df, right=links_df,
                                     how='left',
                                     left_on='entry_text_lower',
                                     right_on='entry_text_lower_links',
                                     )

print(catalog_cleaned_df_joined.columns)
print(catalog_cleaned_df_joined[['entry_text_lower', 'entry_links']][0:3])
# print(catalog_cleaned_df_joined[~catalog_cleaned_df_joined['entry_links'].isnull()])
# print(catalog_cleaned_df_joined['entry_links'].unique().tolist())
catalog_cleaned_df_joined = catalog_cleaned_df_joined[['entry_uuid', 'entry_links']]

catalog_cleaned_df_final = pd.read_csv('data/cleaned/catalog_cleaned.csv')
final_merged_df = pd.merge(left=catalog_cleaned_df_final, right=catalog_cleaned_df_joined,
                           how='left',
                           on='entry_uuid')

print(final_merged_df.iloc[0])

final_merged_df.to_csv('data/cleaned/database_cleaned_w_links.csv', index=False)

