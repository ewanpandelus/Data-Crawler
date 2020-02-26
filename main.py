
import tweepy as tweepy
import json
import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import csv
from textblob import TextBlob

with open('keys.json', 'r') as keys:
    data = keys.read()

# parse file
obj = json.loads(data)


class Crawler:
    def __init__(self, status):
        print(status.text)
        print(self.get_tweet_sentiment(status))
        self.crawlFriends(status)
        # self.crawlFollowers(status)

    def crawlFriends(self, status):
        for user in tweepy.Cursor(api.friends, screen_name=status.user.name).items():
            print('friend: ' + user.screen_name)
            friend_tweets = api.user_timeline(
                screen_name=user.screen_name, count=10)
            outtweets = [[tweet.id_str, tweet.created_at,
                          tweet.text.encode("utf-8")] for tweet in friend_tweets]

    def crawlFollowers(self, status):
        for user in tweepy.Cursor(api.followers, screen_name=status.user.name).items():
            print('follower: ' + user.screen_name)

    def clean_tweet(self, tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())

    def get_tweet_sentiment(self, tweet):
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        crawler = Crawler(status)


auth = tw.OAuthHandler(obj["consumer_key"], obj["consumer_secret"])
auth.set_access_token(obj["access_token"], obj["access_token_secret"])
api = tweepy.API(auth, wait_on_rate_limit=True)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['boris'])
