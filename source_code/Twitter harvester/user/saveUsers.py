import couchdb

couch = couchdb.Server('http://couchdb:aa2447@localhost:5984')
db_stream = couch['db_arabic_streamer']
db_hist = couch['db_arabic_historic']
db_user = couch['db_arabic__user']

for row in db_stream:
    tweet = db_stream[row]
    id_user = tweet['user']['id_str']
    if id_user not in db_user:
        pro_tweet = {}
        pro_tweet['flag'] = 0
        db_user[id_user] = pro_tweet

for row in db_hist:
    tweet = db_hist[row]
    id_user = tweet['user']['id_str']
    if id_user not in db_user:
        pro_tweet = {}
        pro_tweet['flag'] = 0
        db_user[id_user] = pro_tweet
