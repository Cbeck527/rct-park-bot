"""
Retweet awesome @RCTGuests Account

INVOKED: Every couple hours (ish)

Load @RCTGuests timeline and retweet the latest update.
"""
import os

from TwitterAPI import TwitterAPI


def handler(event, _):
    api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )
    r = api.request('statuses/user_timeline', {'screen_name': 'RCTGuests'})
    if r.status_code == 200:
        retweet = api.request(f'statuses/retweet/:{r.json()[0].get("id_str")}')
        return retweet.json()
    return "ERROR: Twitter API didn't respond with a 200"
