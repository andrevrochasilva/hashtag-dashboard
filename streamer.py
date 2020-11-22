import tweepy
import spacy
import os

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

# spacy natural language processing english library for filtering stop words
nlp = spacy.load("en_core_web_sm")

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            if not status.extended_tweet['full_text'].startswith('RT'):
                words = nlp(status.extended_tweet['full_text'])
                arr = []
                for word in words:
                    if not word.is_stop and word.pos_ not in ['PUNCT', 'SYM', 'SPACE', 'X']:
                        arr.append(word.text)
                        arr.append(word.pos_)

                print(arr)
        except AttributeError as e:
            if not status.text.startswith('RT'):
                words = nlp(status.text)
                arr = []
                for word in words:
                    if not word.is_stop and word.pos_ not in ['PUNCT', 'SYM', 'SPACE', 'X']:
                        arr.append(word.text)
                        arr.append(word.pos_)
                print(arr)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(languages=["en"], track=['Trump'])
