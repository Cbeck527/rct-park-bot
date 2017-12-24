"""
Break a ride...

INVOKED: Every 8 hours

Sets CloudWatch metric rct-twitter-bot.rct-rides-broken to 1, which will send
SNS notification to be picked up by 'mechanic' function
"""
import rct_util
import os
import boto3
import json

from TwitterAPI import TwitterAPI


def handler(event, _):
    api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN_KEY'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    )
    ride = rct_util.random_ride()
    tweet = ' '.join(
        filter(bool, (ride, rct_util.random_version(), rct_util.STATUS))
    )
    r = api.request('statuses/update', {'status': tweet})
    if r.status_code == 200:
        respond_to = r.json().get('id_str')
        payload = json.dumps({
            'respond_to': respond_to,
            'ride': ride
        })
        s3 = boto3.resource('s3')
        s3.Object('rct-park-bot', 'ride').put(
            Body=payload
        )
        cloudwatch = boto3.client('cloudwatch')
        cloudwatch.put_metric_data(
            Namespace='rct-twitter-bot',
            MetricData=[{
                'MetricName': 'rct-rides-broken',
                'Value': 1,
                # TODO: pad this later
                # 'TimeStamp': SOME_FUTURE_THING
            }]
        )
        return payload
    return "ERROR: Twitter API didn't respond with a 200"
