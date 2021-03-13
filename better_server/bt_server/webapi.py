from flask import Flask, request, current_app
from postgres import PGSQL_DB

from bt_scraper import User
from bt_scraper import Tweet

class WebAPI:
    api = Flask(__name__)
    #api.db =
    def __init__(self, db):
        self.api.db = db

    def run(self):
        self.api.run()
        pass

    @api.route('/user', methods=['POST'])
    def post_user(self):
        body = request.get_json(silent=True)
        if(None == body):
            return "no body"

        req_params = [ 'uid', 'username' ]
        for param in req_params:
            if(not(param in body)):
                return "no " + param

        u = User()
        u.user_id = body['uid']
        u.name = body['username']
        if('bio' in body):
            u.bio = body['bio']

        status = current_app.db.insert_user(u)
        if (200 == status):
            return "ok"
    
        return "couldn't insert"

    @api.route('/tweet', methods=['POST'])
    def post_tweet():
        body = request.get_json(silent=True)
        if(None == body):
            return "no body"

        req_params = [ 'tid', 'author_id', 'parent_id', 'timestamp', 'text' ]
        for param in req_params:
            if(not(param in body)):
                return "no " + param

        t = Tweet()
        t.tweet_id = body['tid']
        t.author_id = body['author_id']
        t.parent_id = body['parent_id']
        t.timestamp = body['timestamp']
        t.text = body['text']

        status = current_app.db.insert_tweet(t)
    
        if(200 == status):
            return "ok"

        return "couldn't insert"

    @api.route('/user', methods=['GET'])
    def get_user():
        return "error"

    # currently assumes getting by ID since no other method is implemented
    @api.route('/user/<uid>', methods=['GET'])
    def get_user_by_id(uid):
        user = current_app.db.get_user_by_id(uid)
        if(None != user):
            return user.to_json()
        return "error"

    @api.route('/tweet', methods=['GET'])
    def get_tweet():
        return "error"

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
        return "error"

if __name__ == '__main__':
    a = WebAPI(PGSQL_DB("bettertwitter", "localhost", 5432, "bettertwitter", "123"))

    a.run()
