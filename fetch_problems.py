import json
import requests
import sqlite3
import os
import pandas as pd

import packages


table_name: str = "problems"

# Hit the web api of Atcoder Problems
# https://github.com/kenkoooo/AtCoderProblems/blob/master/doc/api.md
json_urls = ["https://kenkoooo.com/atcoder/resources/problem-models.json",
            "https://kenkoooo.com/atcoder/resources/merged-problems.json"]


def getjson(url: str, save_cache: bool = False) -> str:
    """
    Fetch json data with web api

    Parameters
    ----------
    url: str
        URL of json file
    save_cache: bool
        Whether save the json file to the folder

    Returns
    -------
    response.text: str
        JSON data as a string
    """
    # Hit the web api
    response = requests.get(url)

    # When failed to hit the web api
    if response.status_code != 200:
        print(f"Cannot fetch the data (status code: {response.status_code})")
        exit()

    # Save the fetched json data
    if save_cache:
        with open(url.rsplit("/", 1)[1], "w", encoding="UTF-8") as f:
            f.write(response.text)

    # Return the json data (str) extracted from the response
    return response.text


# Move to directory in which this file exists
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Make connection with DB
db_conn = sqlite3.connect(packages.settings.problems_db_name)

# Fetch the json and convert to pandas dataframe
df_model = pd.read_json(getjson(json_urls[0]))
df_detail = pd.read_json(getjson(json_urls[1]))

# Transpose
df_model = df_model.T

# Merge the two dataframes into one with problem names as a key
df = pd.merge(df_model, df_detail, left_index=True, right_on="id")

# Update problems table
df.to_sql(table_name, db_conn, if_exists="replace")

# Close the connection with DB
db_conn.close()