import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

consumer_key = "DZC5B3agcSsbGbrI9JQ1xhSCr"
consumer_secret = "7E0oyANOjc4zdBZ2xsgGCOQtixArmE2zOKdKElcyEJnThJrUQT"
access_token = "1173508449805754368-v08F2Qskwtz0ntIgLncvGRwXOxrdSl"
access_token_secret = "VAYw5ovNjoPIoLj3YtIVIaihPVKjgkvEpfaDN2kWbEqiU"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

npn_dict = {
    "Positive": 0,
    "Neutral": 0,
    "Negative": 0,
    "tweets": ''
}


def get_dict():
    return npn_dict


def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        npn_dict["Positive"] += 1

    elif sentiment_dict['compound'] <= - 0.05:
        npn_dict["Negative"] += 1

    else:
        npn_dict["Neutral"] += 1


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        sentiment_scores(tweet.text)
        time.sleep(1)
        npn_dict['tweets'] = tweet.text

    def on_error(self, status):
        print("Error detected")

