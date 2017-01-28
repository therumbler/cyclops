import os
import random
import string
import json
import logging

log = logging.getLogger("dixit")

class Database():
    def __init__(self):
        if "/lib" in os.getcwd():
            os.chdir("..")
        self.ID_LENGTH = 10
        self.PATH = "etc/db"

    def get_random_id(self):
        log.info("creating id")
        return ''.join([random.choice(string.lowercase + string.digits + "_") for _ in range(self.ID_LENGTH)])

    def get_unique_id(self, data_type):
        loaded = True
        max_attempts = 50
        attempts = 0

        identifier = self.get_random_id()
        while loaded and attempts < max_attempts:
            loaded = self.load(data_type, identifier)
            identifier = self.get_random_id()
            attempts += 1

        if loaded:
            #we've gotten here 
            return {
                "error": "couldn't create a new identifier after %s attempts" % attempts
            }

        return identifier

    def load(self, data_type, identifier):
        path = "%s/%s/%s.json" % (self.PATH, data_type, identifier)
        try:
            with open(path) as f:
                return json.load(f)
        except IOError, e:
            return False

    def save(self, data_type, data, identifier = False):
        if not identifier:
            #get a new unique identifier
            if "identifier" in data.keys() and data["identifier"]:
                identifier = data["identifier"]
            else:
                identifier = self.get_unique_id(data_type)

        if "identifier" not in data.keys() or not data.get("identifier"):
            data["identifier"] = identifier

        #check to see if the folder exists
        #if not, create it
        path = "%s/%s" % (self.PATH, data_type)
        if not os.path.exists(path):
            print "creating", path
            os.mkdir(path)

        #add the identifier to the saved data
        if "identifier" not in data.keys():
            data["identifier"] = identifier

        path = "%s/%s/%s.json" % (self.PATH, data_type, identifier)
        with open(path, "w") as f:
            f.write(json.dumps(data, indent = 4))

        return data

def main():
    db = Database()

    print db.get_random_id()

    #print db.load("games", "hi1zpsx99x")

    #db.save("game", {"id": "173"})

if __name__ == '__main__':
    main()

