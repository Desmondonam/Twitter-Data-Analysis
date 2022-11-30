import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

import pandas as pd
import json
import csv

# to view all columns
pd.set_option("display.max.columns", None)

# credentials from https://apps.twitter.com/
consumerKey = '#'
consumerSecret = '#'
accessToken = '#'
accessTokenSecret = '#'

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# from google.colab import drive
# drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/Batch5_Twitter_Data

hashtags = ["#inflation", "#fuelprice", "#fuelpricehike", "#fuelprices", "#fuelshortage", "#foodprice", "#oilprice", "#oilprices", "#cookingoilprice",
            "#unemployment", "#unemploymentrate", "#economiccrisis", "#economichardship"]

# kenya, geocode="0.0236,37.9062,530km"
# south africa, geocode="-26.22081,28.03239,400km"
# nigeria, geocode="6.48937,3.37709,900km"

# Add gecode variable for country specific data and remove it for general data.
names = []
for hashtag in hashtags:
    tweets = tweepy.Cursor(api.search, q=hashtag, wait_on_rate_limit=True).items(
        500)  # iterating through 500 tweets for each hashtag
    users = []
    for status in tweets:
        name = status.user.screen_name
        t = status.text
        users.append(name)
    names.append(users)

screen_names = [y for x in names for y in x]

# merge the lists
names = screen_names
print(len(names))

# drop duplicates
screen_names = list(dict.fromkeys(names))
print(len(screen_names))

df = pd.DataFrame({'names': screen_names})
df.to_csv('data/Economic_Twitter_Data.csv')
df.shape

# Mining 500 tweets per user since january 2022


def get_tweets(screen_names):
    for name in screen_names:
        # Saving the tweets to a json file. The name of the file changes depending on the data being collected

        with open("data/Economic_Twitter_Data.json", 'a') as f:  # open file first
            tweets = tweepy.Cursor(api.user_timeline, screen_name=name,
                                   since='2022-01-01', wait_on_rate_limit=True).items(500)
            for tweet in tweets:
                json.dump(tweet._json, f)  # dump each to file, f
                f.write("\n")
    return print('Done. The keys are: ', list(tweet._json.keys()))


get_tweets(screen_names[0:111])
