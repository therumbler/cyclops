import json
from random import shuffle
from database import Database
from instagram import Instagram

class Game():
    def __init__(self, identifier = False):
        self.db = Database()
        self.players = []
        self.deck = []
        self.identifier = identifier
        if identifier:
            self.load(identifier)

    def add_player(self, player_id):
        if player_id in self.players:
            #player already exists
            
            return False

        self.players.append(player_id)
        self.save()
        return True

    def start(self):
        if len(self.players) < 3:
            return {
                "error": "Cannot start game",
                "description": "Not enough players"
            }
        instagram = Instagram(client_id = "dummy")
        for player_id in self.players:
            media = instagram.get_user_media(player_id)
            for item in media["items"]:
                self.deck.append(item)        

        shuffle(self.deck)

        self.save()

    def to_dict(self):
        return {
            "players": self.players,
            "deck": self.deck,
            "identifier": self.identifier
        }

    def load(self, identifier):
        data = self.db.load("games", identifier)
        if not data:
            return False

        self.players = data["players"]

    def save(self):
        data = self.to_dict()
        data = self.db.save("games", data)
        if not self.identifier:
            self.identifier = data["identifier"]

        return True

    def __str__(self):
        return json.dumps(self.to_dict())

def main():
    game = Game("jioirhj5la")
    game.add_player("therumbler")
    game.add_player("bopperclark")
    game.add_player("anotherexcuse")

    game.start()
if __name__ == '__main__':
    main()