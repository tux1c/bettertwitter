from flask import Flask, request, current_app
import json

from postgres import PGSQL_DB

from bt_scraper import User
from bt_scraper import Tweet

class Message:
    text = ""

    def __init__(self, text):
        self.text = text

    def to_json(self):
        return "{ 'status': \"" + self.text +"\" }"

class WebAPI:
    api = Flask(__name__)
    
    def __init__(self, db):
        self.api.db = db

    def run(self):
        self.api.run()
        pass

    @api.route('/user', methods=['POST'])
    def post_user():
        body = request.get_json(silent=True)
        if(None == body):
            msg = Message("no body")
            return msg.to_json()

        req_params = [ 'uid', 'username' ]
        for param in req_params:
            if(not(param in body)):
                msg = Message("no " + param)
                return msg.to_json()

        u = User()
        u.user_id = body['uid']
        u.name = body['username']
        if('bio' in body):
            u.bio = body['bio']

        status = current_app.db.insert_user(u)
        if (200 == status):
            msg = Message("ok")
            return msg.to_json()
    
        return "couldn't insert"

    @api.route('/tweet', methods=['POST'])
    def post_tweet():
        body = request.get_json(silent=True)
        if(None == body):
            msg = Message("no body")
            return msg.to_json()

        req_params = [ 'tid', 'author_id', 'parent_id', 'timestamp', 'text' ]
        for param in req_params:
            if(not(param in body)):
                msg = Message ("no " + param)
                return msg.to_json()

        t = Tweet()
        t.tweet_id = body['tid']
        t.author_id = body['author_id']
        t.parent_id = body['parent_id']
        t.timestamp = body['timestamp']
        t.text = body['text']

        status = current_app.db.insert_tweet(t)
    
        if(200 == status):
            msg = Message("ok")
            return msg.to_json()

        msg = Message("error inserting user. please refer to server log.")
        return msg.to_json()

    @api.route('/user', methods=['GET'])
    def get_user():
        msg = Message("no user ID to GET. expected url: /user/{id}")
        return msg.to_json()

    # currently assumes getting by ID since no other method is implemented
    @api.route('/user/<uid>', methods=['GET'])
    def get_user_by_id(uid):
        user = current_app.db.get_user_by_id(uid)
        if(None != user):
            return user.to_json()
        msg = Message("couldn't find user with ID: " + uid)
        return msg.to_json()

    @api.route('/user/<uid>/tweets', methods=['GET'])
    def get_user_tweets(uid):
        tweets = current_app.db.get_user_tweets(uid)
        if (None != tweets):
            return json.dumps([tweet.to_dict() for tweet in tweets])
        msg = Message("couldn't find tweets for user ID: " + uid)
        return msg.to_json()

    @api.route('/tweet', methods=['GET'])
    def get_tweet():
        msg = Message("no tweet ID to GET. expected url: /tweet/{id}")
        return msg.to_json()

    # currently assumes getting by ID since no other method is implemented
    @api.route('/tweet/<tid>', methods=['GET'])
    def get_tweet_by_id(tid):
        with_replies = request.args.get('with_replies', default=0, type=int)
        tweet = current_app.db.get_tweet_by_id(tid)
        if(None != tweet):
            if(1 == with_replies):
                replies = current_app.db.get_replies_by_id(tid)
                if (None != replies):
                    tweet.replies = replies
            return tweet.to_json()
        msg = Message("couldn't find tweet with ID: " + tid)
        return msg.to_json()

if __name__ == '__main__':
    a = WebAPI(PGSQL_DB("bettertwitter", "localhost", 5432, "bettertwitter", "123"))

    a.run()
