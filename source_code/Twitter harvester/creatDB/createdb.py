import couchdb
#Local Server
couch = couchdb.Server('http://couchdb:aa2447@localhost:5984')

#Create databases

couch.create('db_arabic_historic')
couch.create('db_arabic_streamer')
couch.create('db_arabic_replies')
couch.create('db_arabic__quoted')
couch.create('db_arabic__user')
couch.create('db_user_tweets')
couch.create('db_tweets_quoted')