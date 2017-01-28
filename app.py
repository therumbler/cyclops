#!venv/bin/python
import json
from flask import Flask, send_from_directory, redirect, request
from lib.cyclops import Cyclops

app = Flask(__name__)
cyclops = Cyclops()

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

"""
@app.route("/<path:filename>")
def index():
    return send_from_directory("public", filename)
"""
@app.route("/login")
def login():
    return redirect(cyclops.get_auth_url()) 

@app.route("/callback")
def callback():
    code = request.args["code"]
    token = cyclops.get_access_token(code)
    return json.dumps(token)

def main():
    app.run("localhost", debug = True)

if __name__ == '__main__':
    main()
