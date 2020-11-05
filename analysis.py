import pandas as pd
import nltk

# TO EXPLORE:
# entries containing "tweet" (Twitter-related controversies)
# Mueller report
# countries
# Russia, China, North Korea, Iran
# COVID/coronavirus
# Trumpworld - family, campaign
# for names -- group last name with full name (eg: some entries may refer to 'Robert Mueller', others 'Mueller' -- both should be grouped together)

catalog_df = pd.read_csv("data/cleaned/catalog_cleaned.csv")

catalog_df_sample = catalog_df.sample(n=100)


def count_entries_day(df):
    daily_count_df = df.groupby(by='entry_date_dt')['entry_uuid'].agg('count')

    print(daily_count_df)


count_entries_day(catalog_df)


