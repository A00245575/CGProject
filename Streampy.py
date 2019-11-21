import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from datetime import datetime
import time

consumer_key = "DZC5B3agcSsbGbrI9JQ1xhSCr"
consumer_secret = "7E0oyANOjc4zdBZ2xsgGCOQtixArmE2zOKdKElcyEJnThJrUQT"
access_token = "1173508449805754368-v08F2Qskwtz0ntIgLncvGRwXOxrdSl"
access_token_secret = "VAYw5ovNjoPIoLj3YtIVIaihPVKjgkvEpfaDN2kWbEqiU"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

npn_dict = {
                "Positive":0,
                "Neutral":0,
                "Negative":0
            }


def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        npn_dict["Positive"] += 1;
        return "Positive"

    elif sentiment_dict['compound'] <= - 0.05:
        npn_dict["Negative"] += 1;
        return "Negative"

    else:
        npn_dict["Neutral"] += 1;
        return "Neutral"


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        super().__init__(api)
        self.api = api
        self.me = api.me()
        row = ["Time", "Sentiment"]
        with open('twitter.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

    def on_status(self, tweet):
        sentiment = sentiment_scores(tweet.text)
        now = datetime.now()  # time object
        row = [now, sentiment]
        with open('twitter.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        time.sleep(1)


        print("{}".format("Positive: "), npn_dict["Positive"])
        print(type(npn_dict["Positive"]))


        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")




if __name__ == "__main__":
    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=["Trump"], languages=["en"])





