#!/usr/bin/env python
# encoding: utf-8
#Taken from: https://gist.github.com/yanofsky/5436496

import tweepy #https://github.com/tweepy/tweepy
import csv
from pymongo import MongoClient
import json
from tuiteros import *

client = MongoClient('localhost', 27017)
db = client['taller3']
collection_tweets = db['tweets']

# load from file:
with open('conf.json', 'r') as f:
    try:
        conf = json.load(f)
    except ValueError:
        conf = {}
#Twitter API credentials
consumer_key = conf["consumer_key"]
consumer_secret = conf["consumer_secret"]
access_key = conf["access_key"]
access_secret = conf["access_secret"]


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=199)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		#print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=199,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	for tweet in alltweets:
		print "tuit insertado.."
		print tweet._json
		collection_tweets.insert(tweet._json)
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	lista_tuiteros = get_tuiteros()
	lista_actual = collection_tweets.distinct("user.screen_name")
	conjunto_actual = set(lista_actual)
	print lista_actual
	for tuitero in lista_tuiteros:
		if tuitero in conjunto_actual:
			print "Username ya esta"
		else:
			print "Obteniendo tuits de: " + tuitero
			get_all_tweets(tuitero)
