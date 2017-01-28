import urllib2
import json
from urllib import urlencode

class Instagram():
    def __init__(self, client_id = False, client_secret = False, redirect_uri = False, access_token = False):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.access_token = access_token
        if not access_token and not client_id:
            raise Exception("Instagram must be instantiated with either a client_id or an access_token")

        self.base_url = "https://api.instagram.com/v1"

    def get_user_media(self, username):
        url = "https://instagram.com/%s/media" %username
        response = urllib2.urlopen(url)
        return json.load(response)

    def get_auth_url(self):
        return "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=code&scope=public_content" % (self.client_id, self.redirect_uri)

    def get_access_token(self, code):
        url = "https://api.instagram.com/oauth/access_token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        request = urllib2.Request(url, urlencode(data))
        response = urllib2.urlopen(request)

        return json.load(response)

    def get(self, endpoint, **params):
        if "access_token" not in params.keys():
            params["access_token" ] = self.access_token

        querystring = urlencode(params)
        url = "%s/%s?%s" %(self.base_url, endpoint, querystring)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            response = e
        return json.load(response)

def main():
    with open("../etc/config/config.json") as f:
        config = json.load(f)

    client_id = config["instagram"]["client_id"]
    client_secret = config["instagram"]["client_secret"]
    redirect_uri = "http://localhost:5000/callback"
    access_token = "30746200.dd37349.4886cbba793248cea881370ea4388592"
    instagram  = Instagram(client_id, client_secret, redirect_uri, access_token)

    #response = instagram.get("users/54206/media/recent")
    #response = instagram.get("users/search", q = 'christine')
    response  = instagram.get("media/1432789066294640043_30595197")
    #response = instagram.get_user_media("anotherexcuse")
    #print len(response["items"])
    print json.dumps(response, indent = 4)

if __name__ == '__main__':
    main()

