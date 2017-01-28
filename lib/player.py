from database import Database

class Player():
	def __init__(self, instagram_id):
		self.instagram_id = instagram_id
		self.hand = []

	def add_card(self, identifier):
		self.hand.append(identifier)

	def play_card(self, identifier):
		index = self.hand.index(identifier)
		return self.hand.pop(index)

	def to_dict(self):
		return {
			"identifier": self.instagram_id,
			"hand": self.hand
		}

def main():
	#testing
	player = Player(instagram_id = "dummy")

	player.add_card("123")
	player.add_card("124")
	player.add_card("125")

	print player.play_card("123")

if __name__ == '__main__':
	main()