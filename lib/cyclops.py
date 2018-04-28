import logging
import logging.config
import json
import os
from auth import Auth
from game import Game
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
        except IOError as e:
            self.log("Error: %s doesn't exist. Please copy config.json.template to %s and fill in the settings" % (path, path))
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

    def create_fake_user(self, username):
        user_media = self.instagram.get_user_media(username)
        self.log.debug(user_media.keys())
        if len(user_media["items"]) == 0:
            self.log.debug("no items")
            return False

        user = user_media["items"][0]["user"]
        data = {
            "access_token": "%s.abc123" % user["id"],
            "identifier": user["id"],
            "user" : {
                "username": user["username"],
                "bio": "", 
                "website": "", 
                "profile_picture": user["profile_picture"], 
                "full_name": user["full_name"], 
                "id": user["id"]
            }
        }
        
        self.db.save("users", data, identifier = data["identifier"])
        #print json.dumps(user_media, indent = 2)

    def get_status(self, game_id, user_token = False):
        """returns the status from the perspective of a particular user
        """
        if not user_token:
            return {
                "code": 403,
                "description": "No token supplied"
            }
        auth = Auth()
        token = auth.check_token(user_token)
        if not token:
            #no token exists
            return {
                "code": 403,
                "description": "invalid user_token"
            }

     
        game = Game(game_id)
        
        game_status = game.get_status()# = self.db.load("games", game_id)
        
        if not game_status:
            return {
                "error": "invalid game id"
            }
        username = token["user"]["username"]
        
        try:
            player = [p for p in game_status["game"]["players"] if p["username"] == username][0]
        except IndexError as e:
            return {
                "code": 404,
                "description":  "player %s is not in game %s" %(username, game_id)
            }

        return {
            "code": 200,
            "description": "success",
            "game": {
                "player" : player,
                "current_player": game_status["current_player"],
                "players_yet_to_play": game_status["players_yet_to_play"]
                }
        }

def main():
    """let's test somethign out"""
    os.chdir("..")
    cyclops = Cyclops()
    #cyclops.create_fake_user("bopperclark")
   
    game_id = "xv1t6jnmbp"
    game_id = "undefined"
    user_token = "54206.abc123"
    response = cyclops.get_status(game_id=game_id, user_token=user_token)

    print (json.dumps(response, indent=2, separators= (",", ":")))

if __name__ == '__main__':
    main()
