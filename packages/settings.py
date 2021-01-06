import os
import tweepy
import psycopg2
from sqlalchemy import create_engine

# Location of SQLite3 database
problems_db_name = r"db\problems.db"

# Refresh interval (sec)
refresh_interval = 600

def twitter_api() -> tweepy.API:
    """
    Twitter authenication

    Returns
    -------
    api: tweepy.API
        tweepy API object
    """

    CONSUMER_KEY = os.environ['API_KEY']
    CONSUMER_SECRET = os.environ['API_SECRET_KEY']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    return api

def postgre_connection():
    dsn = os.environ['DATABASE_URL']
    return psycopg2.connect(dsn)

sql_engine = create_engine(os.environ['DATABASE_URL'])

word_diff = {\
"灰": {"diff_lower": -9999, "diff_upper": 400},
"茶": {"diff_lower": 400, "diff_upper": 800},
"緑": {"diff_lower": 800, "diff_upper": 1200},
"水": {"diff_lower": 1200, "diff_upper": 1600},
"青": {"diff_lower": 1600, "diff_upper": 2000},
"黃": {"diff_lower": 2000, "diff_upper": 2400},
"橙": {"diff_lower": 2400, "diff_upper": 2800},
"赤": {"diff_lower": 2800, "diff_upper": 3200},
"銅": {"diff_lower": 3200, "diff_upper": 3600},
"銀": {"diff_lower": 3600, "diff_upper": 4000},
"金": {"diff_lower": 4000, "diff_upper": 9999},
"オレンジ": {"diff_lower": 2400, "diff_upper": 2800},

"簡単": {"diff_lower": -9999, "diff_upper": 600},
"普通": {"diff_lower": 600, "diff_upper": 1400},
"難": {"diff_lower": 1400, "diff_upper": 2200},
"灘": {"diff_lower": 2000, "diff_upper": 9999},

"gray": {"diff_lower": -9999, "diff_upper": 400},
"brown": {"diff_lower": 400, "diff_upper": 800},
"green": {"diff_lower": 800, "diff_upper": 1200},
"cyan": {"diff_lower": 1200, "diff_upper": 1600},
"blue": {"diff_lower": 1600, "diff_upper": 2000},
"yellow": {"diff_lower": 2000, "diff_upper": 2400},
"orange": {"diff_lower": 2400, "diff_upper": 2800},
"red": {"diff_lower": 2800, "diff_upper": 3200},
"bronze": {"diff_lower": 3200, "diff_upper": 3600},
"silver": {"diff_lower": 3600, "diff_upper": 4000},
"gold": {"diff_lower": 4000, "diff_upper": 9999},

"easy": {"diff_lower": -9999, "diff_upper": 600},
"moderate": {"diff_lower": 600, "diff_upper": 1400},
"hard": {"diff_lower": 1400, "diff_upper": 2200}
}