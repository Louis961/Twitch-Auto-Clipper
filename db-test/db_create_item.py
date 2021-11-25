from pprint import pprint
import boto3


def put_msg(chat_id, message, channel, timestamp, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.Table('TwitchChat')
    response = table.put_item(
       Item={
            'chat_id': chat_id,
            'message': message,
            'channel': channel,
            'timestamp': timestamp
        }
    )
    return response


if __name__ == '__main__':
    msg_resp = put_msg("12345678", "poggers",
                           "billybob", "timestamp goes here")
    print("Put msg succeeded:")
    pprint(msg_resp, sort_dicts=False)
