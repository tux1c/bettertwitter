import json

class User:
    user_id = ""
    name = ""
    bio = ""

    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self, default=lambda l: l.__dict__, sort_keys=True, indent=4)
