class DB_Abstract:
    # DB Connection constructor
    # INPUT: database information per db implementation (connection info / file path / windows registry / whatever
    # OUTPUT: N/A
    # DESC: constructs the db connection instance and prepares everything necessary to start actively working against the db. if db structure is missing, the function should create it.
    def __init__(self):
        pass

    # Insert a new user into database
    # INPUT: User struct
    # OUTPUT: success status
    # DESC: inserts a new user into the database.
    def insert_user(self, user):
        pass

    # Insert a new tweet into database
    # INPUT: tweet struct
    # OUTPUT: success status
    # DESC: inserts a new tweet into the database.
    def insert_tweet(self, tweet):
        pass

    # Gets a user by their ID
    # INPUT: user ID
    # OUTPUT: user struct or null
    # DESC: builds a user struct out of information pulled from the db.
    def get_user_by_id(self, user_id):
        pass

    # Gets all tweets for user
    # INPUT: user ID
    # OUTPUT: >=1 list of tweets by user, or None
    # DESC: gets all tweets written by a specific user.
    def get_user_tweets(self, uid):
        pass

    # Gets a tweet by it's ID
    # INPUT: tweet ID
    # OUTPUT: tweet struct or null
    # DESC: builds a tweet struct out of information pulled from the db.
    def get_tweet_by_id(self, tweet_id):
        pass

    # Gets all replies for a specific tweet, by tweet ID
    # INPUT: tweet ID
    # OUTPUT: >=1 items list containing tweet replies for a specific tweet, or null.
    # DESC: builds a list of tweet structs containing replies for a specific tweet
    def get_replies_by_id(self, tweet_id):
        pass
