from database import Database

class Auth():
	"""Very simple auth library for Cyclops.

	1. checks that a user exists in the database (based on user_token from Instagram)
	2. returns that user's id and Instagram username
	"""
	def __init__(self):
		self.db = Database()

	def check_token(self, user_token):
		user_ids = self.db.get_all_identifiers(data_type = "users")

		for id in user_ids:
			user = self.db.load("users", id)
			if user_token == user["access_token"]:
				return user

		return False

def main():
	#test code
	auth = Auth()
	user_token = "54206.dd37349.4886cbba793248cea881370ea4388592"
	print auth.check_token(user_token)
	
if __name__ == '__main__':
	main()
