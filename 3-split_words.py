import multiprocessing
import numpy as np
import pandas as pd
import spacy
import sys

def get_words(app):
    doc = nlp(app[3].lower())
    words = []
    words += [token.lemma_ for token in doc if not token.like_num
                                            if not token.like_url
                                            if not token.like_email
                                            if not token.is_oov
                                            if not token.is_stop
                                            if token.is_ascii
                                            if token.is_alpha
                                            if len(token.lemma_) > 2]

    if len(words) < 5:
        return app[0], []

    return app[0], words

df = pd.read_csv(sys.argv[1])
df.dropna(subset=["description"], inplace=True)
df.reset_index(drop=True, inplace=True)
df.insert(loc=2, column='Words', value=np.nan)

nlp = spacy.load("en_core_web_lg")

pool_obj = multiprocessing.Pool()
desc = pool_obj.map(get_words, df.values)

for description in desc:
    app_id = description[0]
    words = description[1]
    df.loc[df["appId"] == app_id, "Words"] = " ".join(words)

df_new = df[df["Words"].map(lambda d: len(d)) > 0]
df_new.reset_index(drop=True, inplace=True)
df_new.to_csv(sys.argv[1], index=False)

