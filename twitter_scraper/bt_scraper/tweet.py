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
