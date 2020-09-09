import GetOldTweets3 as got
import json
import pickle
import os
from io import StringIO
from tqdm import tqdm


def date_to_iso(tweet):
    """Prepare a tweet for serialization by formatting date to ISO."""
    try:
        tweet.date_iso = tweet.date.isoformat()
        del tweet.date
    except AttributeError:
        pass
    return tweet


def get_tweets(query, cache=True):
    """Retrieve the tweets, printing a dot every 100 tweets."""
    with tqdm(total=query.maxTweets) as pbar:
        tweets = got.manager.TweetManager.getTweets(
            query, receiveBuffer=lambda l: pbar.update(100))

    if cache:
        # Pickle them
        with open(os.path.join(DIR, 'wirvsvirus-tweets.pickle'), 'wb') as fd:
            pickle.dump(tweets, fd)

    return tweets


def write_to_json(tweets):
    """Write tweets to JSON file."""
    ts = [date_to_iso(tweet).__dict__ for tweet in tweets]
    with open(os.path.join(DIR, 'wirvsvirus-tweets.json'), 'w') as fd:
        json.dump(tweets, fd)


if __name__ == '__main__':
    MAXTWEETS = 0
    QUERY = '#wirvsvirus'
    DIR = 'tmp'
    
    # Set up the query.
    twitter_query = got.manager.TweetCriteria()
    twitter_query.setQuerySearch(QUERY)
    twitter_query.setMaxTweets(MAXTWEETS)

    # Retrieve.
    tweets = get_tweets(twitter_query)

    # Store to a JSON file.
    write_to_json(tweets)
