import json
import tweepy

consumer_key = "DZC5B3agcSsbGbrI9JQ1xhSCr"
consumer_secret = "7E0oyANOjc4zdBZ2xsgGCOQtixArmE2zOKdKElcyEJnThJrUQT"
access_token = "1173508449805754368-v08F2Qskwtz0ntIgLncvGRwXOxrdSl"
access_token_secret = "VAYw5ovNjoPIoLj3YtIVIaihPVKjgkvEpfaDN2kWbEqiU"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["DnD"], languages=["en"])