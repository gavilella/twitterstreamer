import tweepy
import auth_codes
import re
import json

# Authentication #
auth = tweepy.OAuthHandler(auth_codes.consumer_token, auth_codes.consumer_secret)
auth.set_access_token(auth_codes.access_token, auth_codes.access_secret)

class MyStreamListener(tweepy.StreamListener):
    """
    Classe geral
    """
    def __init__(self):
        self.api = tweepy.API(auth)
        self.numTweets = 0

    # Salvar tweets em arquivo #
    def on_status(self, status, tweet_mode='extended'):
        self.numTweets += 1

        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text

        print(self.numTweets)
        # print(clean_tweet(tweet))
        with open('tweets.txt', 'a') as f:
            tweet = clean_tweet(tweet)+str('|')
            f.write(tweet)


def clean_tweet(raw_text):
    return ' '.join(re.sub("(@)|(\w+:\/\/\S+)", " ", raw_text).split())


# Starts streaming tweets #
myStream = tweepy.streaming.Stream(auth, MyStreamListener())
# Run main class #
go = myStream.filter(languages=['pt'], track=['hoje'])
