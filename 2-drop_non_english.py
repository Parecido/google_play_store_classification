import pandas as pd
import multiprocessing
import spacy
import sys

from bs4 import BeautifulSoup
from spacy.language import Language
from spacy_langdetect import LanguageDetector

def get_lang_detector(nlp, name):
    return LanguageDetector()

def check_english(app):
    soup = BeautifulSoup(app[2])
    doc = nlp(soup.get_text())
    
    if "en" in doc._.language["language"]:
        return app[0], app[2]

    return app[0], ""

df = pd.read_csv(sys.argv[1])
df.dropna(subset=["description"], inplace=True)
df.reset_index(drop=True, inplace=True)

nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)

pool_obj = multiprocessing.Pool()
desc = pool_obj.map(check_english, df.values)

for description in desc:
    app_id = description[0]
    text = description[1]
    df.loc[df["appId"] == app_id, "description"] = text

df.to_csv(sys.argv[1], index=False)

