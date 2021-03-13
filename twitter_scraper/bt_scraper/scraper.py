#!/usr/bin/python3
import re
from json import loads

from rest import run_query

class User:
    name = ""
    identifier = ""
    bio = ""

    def __init__(self, username, user_id, bio):
        name = username
        identifier = user_id
        bio = bio

class BT_Scraper:
    _token = ""

    def __init__(self):
        q = run_query("https://twitter.com/")
        self._token = re.search(r'\("gt=(\d+);', q).group(1)

    def get_user(self, username):
        url = "https://api.twitter.com/graphql/hc-pka9A7gyS3xODIafnrQ/UserByScreenName?variables={\"screen_name\":\"" + username + "\", \"withHighlightedLabel\":false}"

        q = run_query(url, token=self._token)
        u = loads(q)['data']['user']

        user = { 'name': "", 'id': "", 'bio': ""  }

        user['name'] = u['legacy']['name']
        user['id'] = u['rest_id']
        user['bio'] = u['legacy']['description']

        return user

    def get_user_tweets(self, user_id):
        url = "https://twitter.com/i/api/2/timeline/profile/" + user_id + ".json"

        q = run_query(url, token=self._token)
        tweets_raw = loads(q)['globalObjects']['tweets']
        tweets = []

        for tweet_raw in tweets_raw:
            t = tweets_raw[tweet_raw]
            tweet = { 'id': "", 'author_id': "", 'parent_id': "", 'timestamp': "", 'text': "" }
            tweet['id'] = t['id_str']
            tweet['author_id'] = t['user_id_str']
            tweet['text'] = t['text']
            tweet['parent_id'] = t['conversation_id_str']
            tweet['timestamp'] = t['created_at']
            tweets.append(tweet)
        
        return tweets

    def get_tweet_with_replies(self, tweet_id):
        url = "https://twitter.com/i/api/2/timeline/conversation/" + tweet_id + ".json"
    
        q = run_query(url, token=self._token)
        tweets_raw = loads(q)['globalObjects']['tweets']
        tweets = []

        for tweet_raw in tweets_raw:
            t = tweets_raw[tweet_raw]
            tweet = { 'id': "", 'author_id': "", 'parent_id': "", 'timestamp': "", 'text': "" }
            tweet['id'] = t['id_str']
            tweet['author_id'] = t['user_id_str']
            tweet['text'] = t['text']
            tweet['parent_id'] = t['conversation_id_str']
            tweet['timestamp'] = t['created_at']
            tweets.append(tweet)
 
        return tweets
