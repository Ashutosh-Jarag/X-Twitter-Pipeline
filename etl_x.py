import tweepy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load credentials from environment variables
access_key = os.getenv("TWITTER_ACCESS_KEY")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")
consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")

# Debugging: Print the credentials to verify they are loaded
print("Access Key:", access_key)
print("Access Secret:", access_secret)
print("Consumer Key:", consumer_key)
print("Consumer Secret:", consumer_secret)

if not all([access_key, access_secret, consumer_key, consumer_secret]):
    raise ValueError("Twitter API credentials are not set or are invalid.")

# Twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

# Test authentication
try:
    api.verify_credentials()
    print("Authentication successful")
except tweepy.TweepError as e:
    print(f"Authentication failed: {e}")
    exit()

# Fetch tweets
tweets = api.user_timeline(screen_name="@elonmusk", count=200, include_rts=False, tweet_mode="extended")
for tweet in tweets:
    print(tweet.full_text)

