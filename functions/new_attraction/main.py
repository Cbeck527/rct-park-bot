"""
Give a park an award...

INVOKED: Once per day
"""
import os

from TwitterAPI import TwitterAPI

import rct_util


def handler(event, _):
    api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )
    tweet = f"New ride/attraction now available - {rct_util.random_ride()} "
    r = api.request('statuses/update', {'status': tweet})
    if r.status_code == 200:
        return r.text
    return "ERROR: Twitter API didn't respond with a 200"
