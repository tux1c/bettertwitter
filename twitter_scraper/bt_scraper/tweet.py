import json

class Tweet:
    tweet_id = ""
    author_id = ""
    parent_id = ""
    timestamp = ""
    text = ""
    replies = []

    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self, default=lambda l: l.__dict__, sort_keys=True, indent=4)

    def to_dict(self):
        return {
            'tweet_id': self.tweet_id,
            'author_id': self.author_id,
            'parent_id': self.parent_id,
            'timestamp': self.timestamp,
            'text': self.text
        }
