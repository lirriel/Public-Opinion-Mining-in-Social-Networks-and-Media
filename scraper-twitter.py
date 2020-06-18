# from twitter import *
import json
import tweepy

if __name__ == '__main__':
    consumer_key = "consumer_key"
    consumer_secret = "consumer_secret"
    access_token = "access_token"
    access_token_secret = "access_token_secret"

    # Authenticate twitter Api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=5, retry_count=3)
    quieries = []

    for q in quieries:
        c = tweepy.Cursor(api.search, q=q, lang="en")
        c.pages(100000000)  # you can change it make get tweets
        count = 0
        # Lets save the selected part of the tweets inot json
        tweetJson = []
        filename = "twitter_" + q + "_search.json"
        for tweet in c.items():
            if tweet.lang == 'en' and tweet.geo is not None:
                tweetJson.append(tweet._json)
                count += 1

                print(f'{q}: added {count}...')

                if count % 100 == 0:
                    with open(filename, 'w') as f:
                        json.dump(tweetJson, f, ensure_ascii=False)
                if count >= 50000:
                    with open(filename, 'w') as f:
                        json.dump(tweetJson, f, ensure_ascii=False)
                    break
        print(len(tweetJson))
        # dump the data into json format
        with open(filename, 'w') as f:
            json.dump(tweetJson, f, ensure_ascii=False)
