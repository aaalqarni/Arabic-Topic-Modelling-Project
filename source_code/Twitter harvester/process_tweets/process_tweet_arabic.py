# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:58:10 2021

@author: alqarnia
"""
import datetime
import re
import timeit
import pandas as pd
import couchdb
import timeit




#Local Server
couch = couchdb.Server('http://couchdb:aa2447@localhost:5984/')
global db_hist
db_hist = couch['db_user_tweets']
temp_tweets = []





#remove emojies
def strip_emoji(text):
    RE_EMOJI = re.compile(u'([U00002600-U000027BF])|([U0001f300-U0001f64F])|([U0001f680-U0001f6FF])')
    return RE_EMOJI.sub(r'', text)


#def getMainText(tweet):
#    try:
#        text = tweet['full_text']
#    except:
#        text = tweet['text']
#    return text

def getMainText(tweet):
    
    text=""
     
   
    
    if('retweeted_status'  in tweet):
        if("extended_tweet" in tweet["retweeted_status"] ):
            text =  tweet["retweeted_status"]["extended_tweet"]["full_text"]
            #print(text) 
        else:
            text=tweet['text']
        
    elif("extended_tweet" in tweet ):
        
        if("full_text" in tweet["extended_tweet"]):
            text=tweet["extended_tweet"]["full_text"]
    else:    
        text=tweet['text']
    
    return text


def on_status(status):
    if hasattr(status, "retweeted_status"):  # Check if Retweet
        print(status)
        return status

def cleanTweet(tweet):
    
    tweet = re.sub('\n', '  ', str(tweet))
    tweet = re.sub('  ', '  ', str(tweet))
    
    
    return tweet








def tweetProcessor():
    start = timeit.default_timer()
    for row in db_hist:
       
       tweet = db_hist[row]
      
       
       temp_tweets.append(cleanTweet(getMainText(tweet)))
       print(getMainText(tweet))
    stop = timeit.default_timer()
    print('Time: ', stop - start)    
           
           
           
   

if __name__ == '__main__':
    start = timeit.default_timer()
    tweetProcessor()
    df=pd.DataFrame(temp_tweets)
    df.to_csv("arabic_users_tweets.csv",encoding='utf-8-sig')
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    