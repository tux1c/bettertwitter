from flask import Flask, json

def run():
    api = Flask(__name__)
    api.run()
    pass

@api.route('/user', methods=['POST'])
def post_user(user_id, user_name, user_bio):
    pass

@api.route('/tweet', methods=['POST'])
def post_tweet(tweet_id, author_id, parent_id, timestamp, text):
    pass

@api.route('/user', methods=['GET'])
def get_user(uid):
    pass

@api.rout('/tweet', methods=['GET'])
def get_tweet(tid, with_replies=False):
    pass

if __name__ == '__main__':
    run()
