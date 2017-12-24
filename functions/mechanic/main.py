"""
Read SNS Event, grab ride meta info from S3.
 - If the alarm is set (state = ALARM), tweet about a mechanic responding
 - If the alarm is resolved (state = OK), tweet about the ride getting fixed.
"""
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

    s3 = boto3.resource('s3')
    s3_obj = s3.Object('rct-park-bot', 'ride')
    payload = json.loads(s3_obj.get().get('Body').read().decode('utf8'))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    state = message.get('NewStateValue')

    if state == 'ALARM':
        # shits broke, yo
        tweet = f"Mechanic is responding to {payload.get('ride')} breakdown call"
        r = api.request('statuses/update', {
            'status': tweet,
            "in_reply_to_status_id": int(payload.get('respond_to'))
        })
        if r.status_code == 200:
            payload['respond_to'] = r.json().get('id_str')
            s3.Object('rct-park-bot', 'ride').put(
                Body=json.dumps(payload)
            )
            cloudwatch = boto3.client('cloudwatch')
            cloudwatch.put_metric_data(
                Namespace='rct-twitter-bot',
                MetricData=[{
                    'MetricName': 'rct-rides-broken',
                    'Value': 0,
                    # TODO: pad this later
                    # 'TimeStamp': SOME_FUTURE_THING
                }]
            )
            return json.loads(r.text)
        return "ERROR: Twitter API didn't respond with a 200"

    elif state == 'OK':
        # shits fixed, yo
        tweet = f"{payload.get('ride')} has been fixed."
        r = api.request('statuses/update', {
            'status': tweet,
            "in_reply_to_status_id": int(payload.get('respond_to'))
        })
        s3_obj.delete()
        if r.status_code == 200:
            return json.loads(r.text)
        return "ERROR: Twitter API didn't respond with a 200"
