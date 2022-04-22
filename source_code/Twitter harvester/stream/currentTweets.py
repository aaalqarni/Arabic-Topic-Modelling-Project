import tweepy
import json
import time
import couchdb
import os
import geocoder
from datetime import date
from urllib3.exceptions import ProtocolError

from tweepy.streaming import StreamListener

# Local Server
couch = couchdb.Server('http://couchdb:aa2447@localhost:5984/')
global db_stream
global db_rep
global db_quo
global db_hashtag
db_stream = couch['db_arabic_historic']
db_rep = couch['db_arabic_replies']
db_quo = couch['db_arabic__quoted']
db_hashtag=couch['db_hashtags']

API_KEY = 'YGerTBRD9rKTzXgW4qWTRfVkQ'
API_SECRET_KEY = 'Fegey083f0MGkBEk8OZ0P8XmnEf28pyfF4jsmtJ8lnrNeZj3kv'
ACCESS_TOKEN = '455640640-LZXBg60tLN7DSM1ClEnRA5LVSMQRHELJbOboGlXC'
ACCESS_TOKEN_SECRET = '3BzShQJ6CEKSRObWCBNldP6GUFRRslJiXosokpKZQjUyK'

AUS_LAT_MIN = -44
AUS_LON_MIN = 110
AUS_LAT_MAX = -9
AUS_LON_MAX = 156






class MyStreamListener(tweepy.StreamListener):
    
    def on_data(self, data):
        tweet = json.loads(data)
        if 'in_reply_to_status_id_str' in tweet:
            reply = tweet['in_reply_to_status_id']
        else:
             reply=None
            
        try:
            quote = tweet['quoted_status_id']
        except:
            quote = None
           
        if reply is not None:
            saveReply(tweet)
        if quote is not None:
            saveQuoted(tweet)
            print(tweet)
        else:
            saveTweetInDatabase(tweet)

    def on_error(self, status):
        print("Streaming error")


def setCredentials():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)



    
    
    
    
    #1937801
    

def saveReply(tweet):
    pro_tweet = {}
    if 'in_reply_to_status_id_str' in tweet:
        idTweet = tweet['in_reply_to_status_id_str']
        pro_tweet['tweetID_reply'] = tweet['id_str']
        pro_tweet['status'] = 0
        if idTweet not in db_rep:
            db_rep[idTweet] = pro_tweet
            print(idTweet)


def saveQuoted(tweet):
    pro_tweet = {}
    idTweet = tweet['quoted_status_id_str']
    pro_tweet['tweetID_quote'] = tweet['id_str']
    pro_tweet['status'] = 0
    if idTweet not in db_quo:
        db_quo[idTweet] = pro_tweet
        print(pro_tweet)


def saveTweetInDatabase(tweet):
    idTweet = tweet['id_str']
    if idTweet not in db_stream:
        db_stream[idTweet] = tweet
        print(tweet)



def get_trends(api,country):
    from datetime import datetime

   
    trends={}
    trend_list=[]
    try:
        trends=api.trends_place(country)
        for trend in trends[0]['trends']: 
            if trend['tweet_volume'] is not None and trend['tweet_volume'] > 100: 
                trend_list.append((trend['name']))
                today =datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                textfile = open(today, "w",encoding='utf-8')
                for element in  trend_list:
                        textfile.write(element + "\n")
                textfile.close()
        
    except:
        print("--------------1----------------")
                 
            

    return trend_list


def tweetProcessor(api,keywords_list):
    
    #get trended hashtags
    
    
    
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
    try:
        
        kewyords=keywords_list
        while True:
            try:
                my_stream.filter(track=kewyords,is_async=True)
            except (ProtocolError, AttributeError):
                continue
        #my_stream.userstream()
    except:
        print("-----------2-----------------")
        time.sleep(600)
        harvestTweets()

def harvestTweets():
    api_interface = setCredentials()
    keywords=get_trends(api_interface,1937801)
    tweetProcessor(api_interface,keywords)

if __name__ == '__main__':
    harvestTweets()
