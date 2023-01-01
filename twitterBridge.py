import sys
import requests
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = "ZGUdjkFTWuuVFJYDUHoucR1Ry"
CONSUMER_SECRET = "xfFoq1ynIvsnZ7MeipWGT6XMFUx466i1tIaexUKXfqMmoj9EU1"
ACCESS_TOKEN = "1585874163280928769-ZUcNBBnMkW54p7yiUdZQDVT12JewfV"
TOKEN_SECRET = "VDbSxI4F0xylyupXJMwgU54UOfIbAZ2okFdjeoQ9x1Hdy"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKLIkwEAAAAA0KdfM2HZYg9M5bGXZJrExM2x7sg%3DnBSYpThXPQkgAhq2nXHtelNhkGAWQxtrbx1XM1eEjwEplm3MXX"

def link():
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri='oob')
    url = "https://api.twitter.com/oauth/request_token"
    try:
        response = oauth.fetch_request_token(url)
        resource_owner_oauth_token = response.get('oauth_token')
        resource_owner_oauth_token_secret = response.get('oauth_token_secret')
    except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(120)

    authorization_url = f"https://api.twitter.com/oauth/authorize?oauth_token={resource_owner_oauth_token}"

    return authorization_url, resource_owner_oauth_token, resource_owner_oauth_token_secret

def auth(resource_owner_oauth_token, resource_owner_oauth_token_secret, authorization_pin):

    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=resource_owner_oauth_token, 
                            resource_owner_secret=resource_owner_oauth_token_secret, 
                            verifier=authorization_pin)
    
    url = "https://api.twitter.com/oauth/access_token"

    try: 
        response = oauth.fetch_access_token(url)
        access_token = response['oauth_token']
        access_token_secret = response['oauth_token_secret']
        user_id = response['user_id']
        screen_name = response['screen_name']
    except:
        return None

    return [access_token, access_token_secret, user_id, screen_name]

## given a user access_tokem, access_token_secret, user_id, screen_name
## and a tweet id, return if the user has liked the tweet
def likedRetweeted(access_token, access_token_secret, user_id, tweet_id):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/lookup.json?id={tweet_id}&include_entities=true"
    try:
        response = oauth.get(url)
        try:
            hasRetweet = response.json()[0]['retweeted']
        except:
            hasRetweet = False
            
        try:
            hasLike = response.json()[0]['favorited']
        except:
            hasLike = False
        return hasLike, hasRetweet
    except:
        return False, False
    
## see if the last 10 tweets user has posted is a comment on the tweet from tweet_id
def hasCommented(access_token, access_token_secret, tweet_id):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?count=15"
    try:
        response = oauth.get(url)
        for tweet in response.json():
            if tweet['in_reply_to_status_id_str'] == tweet_id:
                return True
        return False
    except:
        return False
    
## see if tweet_id_original is a comment on tweet_id
def isComment(access_token, access_token_secret, tweet_id_original, tweet_id):
    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=access_token, 
                            resource_owner_secret=access_token_secret)
    
    url = f"https://api.twitter.com/1.1/statuses/show.json?id={tweet_id}"
    try:
        response = oauth.get(url)
        if response.json()['in_reply_to_status_id_str'] == tweet_id_original:
            return True
        return False
    except:
        return False