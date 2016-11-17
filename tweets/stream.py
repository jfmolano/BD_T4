#Tomado de: http://code.runnable.com/Us9rrMiTWf9bAAW3/how-to-stream-data-from-twitter-with-tweepy-for-python
import tweepy
from pymongo import MongoClient
import json
from tuiteros import *

# load from file:
with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}
#Twitter API credentials
consumer_key = conf["consumer_key"]
consumer_secret = conf["consumer_secret"]
access_token = conf["access_key"]
access_token_secret = conf["access_secret"]
ip_mongo = conf["ip_mongo"]

client = MongoClient(ip_mongo, 27017)
db = client['Grupo03']
collection_tweets = db['tweets_taller4']

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
	try:
        	collection_tweets.insert(decoded)
	except:
		print "error"
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print "Showing all new tweets for :"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    lista_filtro = []
    lista_tuiteros = get_tuiteros()
    lista_filtro = lista_filtro + lista_tuiteros
    stream.filter(track=lista_filtro)
