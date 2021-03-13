import configparser
import threading
import time
import re
import os.path

from postgres import PGSQL_DB
from bt_scraper import User
from bt_scraper import Tweet

from bt_scraper import Scraper

#from . import webapi
from webapi import WebAPI

class BTServer:
    db = None
    #db = PGSQL_DB("bettertwitter", "localhost", 5432, "bettertwitter", "123")
    cfg = configparser.ConfigParser()
    
    def thrd_scrape_users(self, users, sleep_time):
        scraper = Scraper()

        while True:
            for u in users:
                user = scraper.get_user(u)
                if(None == self.db.get_user_by_id(user.user_id)):
                    self.db.insert_user(user)

                tweets = scraper.get_user_tweets(user.user_id)
                tweets_to_add = []
                
                for t in tweets:
                    if(None == self.db.get_tweet_by_id(t.tweet_id)):
                        tweets_to_add.append(t.tweet_id)

                for t in tweets_to_add:
                    thread = scraper.get_tweet_with_replies(t)
                    for twt in thread:
                        status = self.db.insert_tweet(twt)
                        if (200 != status):
                            print("Error inserting tweet. Refer to log")
            
            time.sleep(sleep_time)

    def sanitize_users(self, users):
        list_users = users.split(',')
        list_sanitized_users = []
        for user in list_users:
            list_sanitized_users.append(re.sub(r'\W+', '', user))
        return list_sanitized_users

    def run(self):
        if(not(os.path.exists("config.ini"))):
            self.cfg['Twitter'] = { 'users': "UNWatch,Twitter" }
            self.cfg['Technical'] = { 
                                        'time_interval': 3600,
                                        'db_name': "bettertwitter",
                                        'db_host': "localhost",
                                        'db_port': 5432,
                                        'db_user': "bettertwitter",
                                        'db_pass': "123"
                                    }
            with open('config.ini', 'w') as configfile:
                self.cfg.write(configfile)
        else:
           self.cfg.read("config.ini") 

        list_users = self.sanitize_users(self.cfg['Twitter']['users'])


        #self.db = PGSQL_DB("bettertwitter", "localhost", 5432, "bettertwitter", "123")
        self.db = PGSQL_DB(
                            self.cfg['Technical']['db_name'],
                            self.cfg['Technical']['db_host'],
                            int(self.cfg['Technical']['db_port']),
                            self.cfg['Technical']['db_user'],
                            self.cfg['Technical']['db_pass']
                        )

        scrape = threading.Thread(target=self.thrd_scrape_users, args=(list_users, int(self.cfg['Technical']['time_interval'])))
        scrape.start()

        api = WebAPI(self.db)
        api.run()

if __name__ == '__main__':
    serv = BTServer()
    serv.run()
