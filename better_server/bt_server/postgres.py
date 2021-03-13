from db_abstract import DB_Abstract
from user import User
from tweet import Tweet

from pg import DB

class PGSQL_DB(DB_Abstract):
    conn = None

    def __init__(self, dbname, dbhost, dbport, dbuser, dbpass):
        try:
            self.conn = DB(dbname=dbname, host=dbhost, port=dbport, user=dbuser, passwd=dbpass)
        except:
            print("sth wrong bro")
            self.conn = None

        if (None != self.conn):
            tables = self.conn.get_tables()
            if (not("public.users" in tables)):
                try:
                    self.conn.query("CREATE TABLE users(uid bigint primary key, name text, bio text)")
                except:
                    print("sth wrong bro")
                    self.conn = None
            if (not("public.tweets" in tables)):
                try:
                    self.conn.query("CREATE TABLE tweets(tid bigint primary key, author_id bigint, parent_id bigint, timestamp bigint, text text)")
                except:
                    print("sth wrong bro")
                    self.conn = None

    def insert_user(self, user):
        if (not(type(user) is User)):
            print("type isn't user")
            return 400

        if("" == user.user_id or "" == user.name):
            print("empty user")
            return 400

        if(None == self.conn):
            print("no connection")
            return 400;

        try:
            self.conn.insert('users', {'uid': user.user_id, 'name': user.name, 'bio': user.bio})
        except:
            print("sth wrong bro inser_user")
            return 400

        return 200

    def insert_tweet(self, tweet):
        if(not(type(tweet) is Tweet)):
            print("type isn't Tweet")
            return 400

        if("" == tweet.tweet_id or "" == tweet.author_id or "" == tweet.parent_id or "" == tweet.timestamp or "" == tweet.text):
            print("empty tweet")
            return 400

        if(None == self.conn):
            print("no connection")
            return 400

        try:
            self.conn.insert('tweets', {'tid':tweet.tweet_id, 'author_id':tweet.author_id, 'parent_id':tweet.parent_id, 'timestamp':tweet.timestamp, 'text':tweet.text})
        except:
            print("sth wrong bro insert_tweet")
            return 400

        return 200

    def get_user_by_id(self, user_id):
        if("" == user_id):
            print("empty user_id")
            return None

        if(None == self.conn):
            print("no connection")
            return None

        try:
           u = self.conn.get('users', {'uid': user_id})
        except:
            print("sth wrong brong get_user_by_id")
            return None

        user = User()
        user.user_id = u['uid']
        user.name = u['name']
        user.bio = u['bio']

        return user

    def get_tweet_by_id(self, tweet_id):
        if(None == self.conn):
            print("no connection")
            return None

        try:
            t = self.conn.get('tweets', {'tid': tweet_id})
        except:
            print("sth wrong bro get_tweet_by_id")
            return None

        tweet = Tweet()
        tweet.tweet_id = t['tid']
        tweet.author_id = t['author_id']
        tweet.parent_id = t['parent_id']
        tweet.timestamp = t['timestamp']
        tweet.text = t['text']

        return tweet

    def get_replies_by_id(self, tweet_id):
        if(None == self.conn):
            print("no connection")
            return None

        try:
            t = self.conn.get_as_list('tweets', where="parent_id = " + tweet_id)
        except:
            print("sth wrong bro get_replies_by_id")
            return None

        tweets = []
        for tweet in t:
            if(tweet[0] != tweet[2]):
                new_tweet = Tweet()
                new_tweet.tweet_id = tweet[0]
                new_tweet.author_id = tweet[1]
                new_tweet.parent_id = tweet[2]
                new_tweet.timestamp = tweet[3]
                new_tweet.text = tweet[4]
                tweets.append(new_tweet)

        if(0 == len(tweets)):
            return None

        return tweets
