#!/usr/bin/python3
import re
from json import loads
from dateutil.parser import parse

from .rest import run_query
from .user import User
from .tweet import Tweet

class Scraper:
    _token = ""

    def __init__(self):
        q = run_query("https://twitter.com/")
        self._token = re.search(r'\("gt=(\d+);', q).group(1)

    def get_user(self, username):
        url = "https://api.twitter.com/graphql/hc-pka9A7gyS3xODIafnrQ/UserByScreenName?variables={\"screen_name\":\"" + username + "\", \"withHighlightedLabel\":false}"

        q = run_query(url, token=self._token)
        u = loads(q)['data']['user']

        user = User()

        user.name = u['legacy']['name']
        user.user_id = u['rest_id']
        user.bio = u['legacy']['description']

        return user

    def get_user_tweets(self, user_id):
        url = "https://twitter.com/i/api/2/timeline/profile/" + user_id + ".json"

        q = run_query(url, token=self._token)
        tweets_raw = loads(q)['globalObjects']['tweets']
        tweets = []

        for tweet_raw in tweets_raw:
            t = tweets_raw[tweet_raw]
            tweet = Tweet()
            tweet.tweet_id = t['id_str']
            tweet.author_id = t['user_id_str']
            tweet.text = t['text']
            tweet.parent_id = t['conversation_id_str']
            tweet.timestamp = int(parse(t['created_at']).strftime("%s"))
            tweets.append(tweet)
 
        return tweets

    def get_tweet_with_replies(self, tweet_id):
        url = "https://twitter.com/i/api/2/timeline/conversation/" + tweet_id + ".json"
    
        q = run_query(url, token=self._token)
        tweets_raw = loads(q)['globalObjects']['tweets']
        tweets = []

        for tweet_raw in tweets_raw:
            t = tweets_raw[tweet_raw]
            tweet = Tweet()
            tweet.tweet_id = t['id_str']
            tweet.author_id = t['user_id_str']
            tweet.text = t['text']
            tweet.parent_id = t['conversation_id_str']
            tweet.timestamp = int(parse(t['created_at']).strftime("%s"))
            tweets.append(tweet)
 
        return tweets
