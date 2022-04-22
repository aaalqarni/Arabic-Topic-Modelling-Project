import tweepy
import time
import couchdb


#Local Server
couch = couchdb.Server('http://couchdb:aa2447@localhost:5984/')
global db_hist
global db_rep
global db_quo
db_hist = couch['db_tweets_quoted']
db_rep = couch['db_arabic_replies']
db_quo = couch['db_arabic__quoted']

API_KEY = 'YGerTBRD9rKTzXgW4qWTRfVkQ'
API_SECRET_KEY = 'Fegey083f0MGkBEk8OZ0P8XmnEf28pyfF4jsmtJ8lnrNeZj3kv'
ACCESS_TOKEN = '455640640-LZXBg60tLN7DSM1ClEnRA5LVSMQRHELJbOboGlXC'
ACCESS_TOKEN_SECRET = '3BzShQJ6CEKSRObWCBNldP6GUFRRslJiXosokpKZQjUyK'

def setCredentials():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def saveReply(tweet):
    pro_tweet = {}
    idTweet = tweet['in_reply_to_status_id_str']
    pro_tweet['tweetID_reply'] = tweet['id_str']
    pro_tweet['status'] = 0
    if idTweet not in db_rep:
        db_rep[idTweet] = pro_tweet

def saveQuoted(tweet):
    pro_tweet = {}
    idTweet = tweet['id_str']
    pro_tweet['tweetID_quote'] = tweet['quoted_status_id_str']
    pro_tweet['status'] = 0
    if idTweet not in db_quo:
        db_quo[idTweet] = pro_tweet


def saveTweetInDatabase(tweet):
    idTweet = tweet['id_str']
    if idTweet not in db_hist:
        db_hist[idTweet] = tweet
        print(idTweet)


def getMainText(tweet):
    try:
        text = tweet['full_text']
    except:
        text = tweet['text']
    return text

def tweetProcessor(api_interface):
    #global quoteOne
    for row in db_quo:
        quoteOne = None
        rep = db_quo[row]
        if rep['status'] == 0:
            try:
                statusOne = api_interface.get_status(row, tweet_mode="extended")
                tweetOne = statusOne._json
            except:
                tweetOne = None

            try:
                statusTwo = api_interface.get_status(db_quo[row]['tweetID_quote'], tweet_mode="extended")
                tweetTwo = statusTwo._json
            except:
                tweetTwo = None

            if (tweetOne is not None) and (tweetTwo is not None):
                try:
                    quoteOne = tweetOne['quoted_status']['id_str']
                except:
                    quoteOne = None

                try:
                    quoteTwo = tweetTwo['quoted_status']['id_str']
                except:
                    quoteTwo = None

                if quoteTwo == tweetOne['id_str']:
                    saveTweetInDatabase(tweetOne)
                    tweetTwo['tweet_quoted_to'] = getMainText(tweetOne)
                    saveTweetInDatabase(tweetTwo)
                elif quoteOne == tweetTwo['id_str']:
                    saveTweetInDatabase(tweetTwo)
                    tweetOne['tweet_quoted_to'] = getMainText(tweetTwo)
                    saveTweetInDatabase(tweetOne)
            elif (tweetOne is not None) and quoteOne is None:
                saveTweetInDatabase(tweetOne)
            elif (tweetTwo is not None) and quoteTwo is None:
                saveTweetInDatabase(tweetTwo)
        rep['status'] = 1
        db_quo.save(rep)

def harvestTweets():
    api_interface = setCredentials()
    tweetProcessor(api_interface)

if __name__ == '__main__':
    harvestTweets()
