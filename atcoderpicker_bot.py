import sqlite3
import os
import pandas as pd
import tweepy
import datetime

import packages

# For debug purpose
# pd.set_option('display.max_columns', 100)

def geturl(problem: pd.DataFrame) -> str:
    """
    Generate URL from oneline dataframe of a problem

    Parameters
    ----------
    problem: Dataframe
        Problem data as one specific line of dataframe
    
    Returns
    -------
    url: str
        URL of corresponding problem on AtCoder
    """

    name = problem.iloc[0]["id"]

    # contest_name = name.rsplit("_", 1)[0].replace("_", "-")
    contest_name = problem.iloc[0]["contest_id"]

    url = "https://atcoder.jp/contests/" + contest_name + "/tasks/" + name

    return url


# Move to directory in which this file exists
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Make connection with DB
db_conn = sqlite3.connect(packages.settings.problems_db_name)

# Read the problems table to dataframe
df = pd.read_sql("SELECT * FROM problems", db_conn)

# Take user input
# message: str = input()
api = packages.settings.twitter_api()
mentions = api.mentions_timeline(count=15)

# For each mentions
for mention in mentions:

    # UTC Timezone
    UTC = datetime.timezone(datetime.timedelta(hours=0), "UTC")

    mention_timestamp = datetime.datetime.fromtimestamp(mention.created_at.timestamp(), UTC)
    current_time = datetime.datetime.now(UTC)

    if current_time - mention_timestamp > datetime.timedelta(seconds=packages.settings.refresh_interval):
        continue

    # List for piling up difficulty ranges
    diff_ranges = []

    # Initialize mask with all True
    diff_mask = df["difficulty"] != None

    # Find keyword in the given message
    for key in packages.settings.word_diff.keys():
        if key in mention.text:
            diff_ranges.append(packages.settings.word_diff[key])

    # Create mask according to given difficulty limitations
    if len(diff_ranges):
        diff_mask = (diff_ranges[0]["diff_lower"] <= df["difficulty"]) & (df["difficulty"] < diff_ranges[0]["diff_upper"])

        for diff_range in diff_ranges[1:]:
            diff_mask = diff_mask | ((diff_range["diff_lower"] <= df["difficulty"]) & (df["difficulty"] < diff_range["diff_upper"]))

    # Extract data that meets the conditions
    df_ = df[diff_mask]

    # Pick a problem!
    chosen_problem = df_.sample()

    response = f"@{mention.user.screen_name} はいよ！\n"


    response += f'{chosen_problem.iloc[0]["contest_id"].upper()} {chosen_problem.iloc[0]["title"]}\n'


    # print(f'Diff: {packages.atrating.modrate(chosen_problem.iloc[0]["difficulty"])}')

    response += geturl(chosen_problem)

    print(mention.text)
    print(f"@{mention.user.screen_name} はいよ！\n")
    print(f'{chosen_problem.iloc[0]["contest_id"].upper()} {chosen_problem.iloc[0]["title"]}')
    print(geturl(chosen_problem))

    api.update_status(status=response, in_reply_to_status_id=mention.id)


# Close connection with DB
db_conn.close()