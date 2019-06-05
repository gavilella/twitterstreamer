import tweepy
import time
import auth_codes


def download_tweets(id_file, sentiment):
    with open(id_file) as infile:
        for tweet_id in infile:
            tweet_id = tweet_id.strip()

            if db.exist_tweet(tweet_id):
                print("tweet com id: ", tweet_id, "já foi capturado")
                continue

            try:
                tweet = api.get_status(tweet_id)
                db.add_tweet(tweet, sentiment)
            except tweepy.error.TweepError:
                print("tweet com id: ", tweet_id, "não está disponível")

            time.sleep(1)


auth = tweepy.OAuthHandler(auth_codes.consumer_token, auth_codes.consumer_secret)
auth.set_access_token(auth_codes.access_token, auth_codes.access_secret)
api = tweepy.API(auth)

print("Capturando tweets positivos ...")
download_tweets("positivos.txt", 1)

print("Capturando tweets negativos ...")
download_tweets("negativos.txt", 0)

print("Fim.")
