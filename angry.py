
import tweepy as tw
import json
import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import pandas as pd
import csv
import re  # regular expression

# read file
with open('keys.json', 'r') as keys:
    data = keys.read()

# parse file
obj = json.loads(data)

# show values


# Authenticate to Twitter
auth = tw.OAuthHandler(obj["consumer_key"], obj["consumer_secret"])
auth.set_access_token(obj["access_token"], obj["access_token_secret"])
# Create API object
api = tw.API(auth, wait_on_rate_limit=True)


def remove_url(txt):

    return " ".join(re.sub(r"([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


search_term = "#angry OR #annoyed OR #rage"

tweets = tw.Cursor(api.search,
                   q=search_term,
                   lang="en",
                   since='2020-02-16').items(150)

# Remove URLs
tweets_no_urls = [remove_url(tweet.text) for tweet in tweets]
