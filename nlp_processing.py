import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk import word_tokenize, pos_tag, pos_tag_sents
from nltk.corpus import stopwords
stop = stopwords.words('english')

catalog_df = pd.read_csv("catalog_cleaned.csv")
catalog_df_sample = catalog_df.sample(n=100)

print(catalog_df_sample['entry_text_split'])


def nltk_process(df):
    # TODO: eliminate stop words
    df['entry_no_stopwords'] = df['entry_text_split'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    df['tokenized_text'] = df['entry_no_stopwords'].apply(word_tokenize)
    df['POS_tagged_text'] = pos_tag_sents(df['entry_text_split'].apply(word_tokenize))

    return df


tokenized_df = nltk_process(catalog_df_sample)


def nltk_token_freq_dict(df):
    unique_tokens = df['tokenized_text'].unique().tolist()
    # TODO: token_hash_dict


tokenized_df.to_csv("nlp_df.csv", index=False)
print(tokenized_df)
