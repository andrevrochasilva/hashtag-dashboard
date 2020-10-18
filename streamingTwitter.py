import os
import mysql.connector as mysql
import tweepy
import spacy
import credentials

# the streaming twitter api requires four pieces of authentication (consumer key, consumer secret, access token,
# access secret) which can be found in your twitter development account details when starting a new project
auth = tweepy.OAuthHandler(credentials.twitter_login['consumer_key'], credentials.twitter_login['consumer_secret'])
auth.set_access_token(credentials.twitter_login['access_token'], credentials.twitter_login['access_secret'])

api = tweepy.API(auth)

# connection to a local mysql database for testing purposes, not necessary for cloud implementation
db = mysql.connect(
    host="localhost",
    user="root",
    passwd=credentials.mysql_pass['password'],
    database="twitterStream"
)

# spacy natural language processing english library for filtering stop words
nlp = spacy.load("en_core_web_sm")

# more mysql for testing, not necessary for cloud implementation
cursor = db.cursor()
sql = "INSERT INTO tweetWords (word) VALUE (%s)"


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
                        cursor.execute(sql, (word.text,))
                        db.commit()
                print(arr)
        except AttributeError as e:
            if not status.text.startswith('RT'):
                words = nlp(status.text)
                arr = []
                for word in words:
                    if not word.is_stop and word.pos_ not in ['PUNCT', 'SYM', 'SPACE', 'X']:
                        arr.append(word.text)
                        arr.append(word.pos_)
                        cursor.execute(sql, (word.text,))
                        db.commit()
                print(arr)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(languages=["en"], track=['Trump'])
