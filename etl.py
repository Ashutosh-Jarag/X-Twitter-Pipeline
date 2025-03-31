import tweepy
import os
import requests
import pandas as pd
import time
import boto3
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Twitter API Credentials
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    raise ValueError("Twitter Bearer Token is not set or is invalid.")

# AWS S3 Credentials
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
s3_bucket_name = "x-etl-bucket"

# Define headers for Twitter API v2
headers = {"Authorization": f"Bearer {bearer_token}"}

# Fetch user ID for the given username
def get_user_id(username):
    user_url = f"https://api.twitter.com/2/users/by/username/{username}"
    response = requests.get(user_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching user ID: {response.json()}")
    return response.json()["data"]["id"]

# Fetch tweets for the given user ID
def fetch_tweets(user_id):
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "tweet.fields": "created_at,public_metrics,text",
        "exclude": "replies,retweets"
    }
    response = requests.get(tweets_url, headers=headers, params=params)
    if response.status_code == 429:
        print("Rate limit exceeded. Waiting for 15 minutes...")
        time.sleep(15 * 60)
        return fetch_tweets(user_id)
    elif response.status_code != 200:
        raise Exception(f"Error fetching tweets: {response.json()}")
    return response.json().get("data", [])

# Upload file to S3
def upload_to_s3(file_name, bucket_name):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    s3_client.upload_file(file_name, bucket_name, file_name)
    print(f"File {file_name} uploaded to S3 bucket {bucket_name}")

# Main function to run the ETL process
def run_twitter_etl():
    username = "elonmusk"
    print(f"Fetching tweets for user: {username}")

    user_id = get_user_id(username)
    print(f"User ID for {username}: {user_id}")

    tweets = fetch_tweets(user_id)
    print(f"Fetched {len(tweets)} tweets.")

    tweet_data = []
    for tweet in tweets:
        refined_tweet = {
            "user": username,
            "text": tweet["text"],
            "created_at": tweet["created_at"],
            "retweet_count": tweet["public_metrics"]["retweet_count"],
            "favorite_count": tweet["public_metrics"]["like_count"]
        }
        tweet_data.append(refined_tweet)

    # Save tweets to a CSV file
    file_name = f"refined_tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df = pd.DataFrame(tweet_data)
    df.to_csv(file_name, index=False)
    print(f"Tweets saved to {file_name}")

    # Upload to S3
    upload_to_s3(file_name, s3_bucket_name)

# Run the ETL function
if __name__ == "__main__":
    run_twitter_etl()
