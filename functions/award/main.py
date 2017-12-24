"""
Give a park an award...

INVOKED: Once per day
"""
import os

import rct_util

from TwitterAPI import TwitterAPI


def handler(event, _):
    api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )
    tweet = f"You park has received the {rct_util.random_award()} "
    r = api.request('statuses/update', {'status': tweet})
    if r.status_code == 200:
        return r.text
    return "ERROR: Twitter API didn't respond with a 200"
