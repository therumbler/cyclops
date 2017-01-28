import logging
import logging.config
import json
import os
from instagram import Instagram
from database import Database

log = None
class Cyclops():
    def __init__(self):
        self.setup_logging()
        success = self.load_config()
        if not success:
            return             

        self.log.debug("debug")
        self.log.info("info")
        self.log.error("error")
        self.db = Database()
        #print self.db.get_random_id()
        
        client_id = self.config["instagram"]["client_id"]
        client_secret = self.config["instagram"]["client_secret"]
        redirect_uri = "http://localhost:5000/callback"
        self.instagram  = Instagram(client_id, client_secret, redirect_uri)

    def load_config(self):
        path = "etc/config/config.json"
        try:
            with open(path) as f:
                self.config = json.load(f)
        except IOError, e:
            print "Error: %s doesn't exist. Please copy config.json.template to %s and fill in the settings" % (path, path)
            return False
        return True
        
    def get_auth_url(self):
        return self.instagram.get_auth_url()

    def setup_logging(self):
        with open("etc/config/logging.json") as f:
            conf = json.load(f)
        logging.config.dictConfig(conf)
        self.log = logging.getLogger("dixit")

    def get_access_token(self, code):
        token = self.instagram.get_access_token(code)

        identifier = token["user"]["id"]
        data = self.db.save("users", token, identifier)

        return data

def main():
    os.chdir("..")
    cyclops = Cyclops()

if __name__ == '__main__':
    main()


