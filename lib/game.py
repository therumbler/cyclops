import json
from random import shuffle
from database import Database
from instagram import Instagram

class Game():
    def __init__(self, identifier = False):
        self.db = Database()
        self.players = []
        self.deck = []
        self.pile = []
        self.phrases = []        
        self.identifier = identifier
        self.actual_card = False
        self.round_number = 0
        self.active_player_index = -1
        if identifier:
            self.load(identifier)

    def add_player(self, username):
        if username in [p["username"] for p in self.players]:
            #player already exists
            print "player already exists"
            return False

        player = {
            "username": username,
            "hand": []
        }

        self.players.append(player)
        self.save()
        return True

    def start(self):
        if len(self.players) < 3:
            return {
                "error": "Cannot start game",
                "description": "Not enough players"
            }
        instagram = Instagram(client_id = "dummy")

        if len(self.deck) == 0:            
            for player in self.players:
                media = instagram.get_user_media(player["username"])
                for item in media["items"]:
                    self.deck.append(item)     

            shuffle(self.deck)

            self.deal()
            self.active_player_index += 1
            self.save()

    def deal(self):
        #deal 5 cards to each player
        for i in range(0, 4):
            for player in self.players:
                if len(player["hand"]) == 5:
                    print "Error: %s already has 5 cards" % player["username"]
                    continue
                card = self.deck.pop()
                player["hand"].append(card)

        self.save()

        return True

    def get_player(self, username):
        try:
            index = [p["username"] for p in self.players].index(username)
        except ValueError, e:
            print "Error: player with id %s does not exist" % username
            return False
 
        return self.players[index]

    def play_card(self, username, card_id):
        if self.active_player_index == -1:
            print "Error: playcard(): game hasn't started"
            return False

        player = self.get_player(username)        
        if not player:
            print "no player found"
            return False

        if len(self.pile) == 0:
            #this is the initial card. ONly allow current player to play
            current_player_username = self.players[self.active_player_index]["username"]
            if username != current_player_username:
                print "Error: The first card hasn't been played yet and %s isn't the current player" % username
                return False

        card_identifiers = [card["id"] for card in player["hand"]]
        try:
            card_index = card_identifiers.index(card_id)
        except ValueError, e:
            card_index = -1
        if card_index < 0:
            print "Error: %s not in %s's hand" % (card_id, player["username"])
            return False


        player_index = [p["username"] for p in self.players].index(player["username"])
        card = self.players[player_index]["hand"].pop(card_index)

        card["player_id"] = player["identifier"]
        self.pile.append(card)

        if len(self.pile) == len(self.players):
            self.finalize()

        self.save()

    def finalize(self):
        self.actual_card = self.pile[0]

        shuffle(self.pile)

        self.active_player_index += 1
        if self.active_player_index > len(self.players) - 1:
            self.active_player_index = 0

    def load(self, identifier):
        data = self.db.load("games", identifier)
        if not data:
            return False

        self.players = data["players"]
        self.deck = data["deck"]
        self.identifier = data["identifier"]
        self.active_player_index = data["active_player_index"]
        self.pile = data["pile"]
        return True

    def save(self):
        data = self.to_dict()
        data = self.db.save("games", data)
        if not self.identifier:
            self.identifier = data["identifier"]

        print "%s saved" % self.identifier
        return self.identifier
    
    def to_dict(self):
        return {
            "players": self.players,
            "deck": self.deck,
            "identifier": self.identifier,
            "active_player_index": self.active_player_index,
            "actual_card" : self.actual_card,
            "pile": self.pile
        }

    def get_status(self):
        if self.active_player_index == -1:
            return {
                "status": "game is yet to begin",
                "game": self.to_dict()
            }

        players_yet_to_play = [p["username"] for p in self.players if len(p["hand"]) == 5]
        
        return {
            "current_player" : self.players[self.active_player_index]["username"],
            "status": "in progress",
            "players_yet_to_play": players_yet_to_play,
            "game": self.to_dict()
        }

    def __str__(self):
        return json.dumps(self.to_dict())

def main():
    game_id = "xv1t6jnmbp"
    game_id = "0kpbzj95pm"
    game = Game(game_id)
    #game.add_player("therumbler")
    #game.add_player("bopperclark")
    #game.add_player("anotherexcuse")

    response = game.get_status() 
    print json.dumps(response, indent = 2)
    card_id = "1411723089812736816_30746200"
    #game.play_card("therumbler", card_id)
  
if __name__ == '__main__':
    main()
