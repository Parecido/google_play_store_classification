import multiprocessing
import pandas as pd
import requests
import sys

from google_play_scraper import app
from time import sleep

def download_data(app_id):
    result = None

    while True:
        try:
            result = app(app_id, lang='en', country='us')
            result = {"appId": result["appId"],
                      "genre": result["genre"],
                      "description": result["description"]}

            break
        except Exception as e:
            if "App not found(404)" in str(e):
                break

            sleep(10)

    return result

df = pd.read_csv(sys.argv[1])

pool_obj = multiprocessing.Pool()
desc = pool_obj.map(download_data, df["App Id"].values)

df_new = pd.DataFrame(data=[])

for data in desc:
    if data != None:
        series = pd.Series(data)
        df_new = pd.concat((df_new, series), axis=1)

df_new.transpose().to_csv(sys.argv[1], index=False)

