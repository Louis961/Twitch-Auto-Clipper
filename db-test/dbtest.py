import boto3
from pprint import pprint

def create_chat_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        #, endpoint_url="http://localhost:8000")
    table = dynamodb.create_table(
        TableName='TwitchChat',
        KeySchema=[
            {
                'AttributeName': 'chat_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'channel',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table status:", table.table_status)
    return table

def put_msg(chat_id, message, channel, timestamp, dynamodb=None):
    if not dynamodb:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        # Instantiate a table resource object without actually
        # creating a DynamoDB table. Note that the attributes of this table
        # are lazy-loaded: a request is not made nor are the attribute
        # values populated until the attributes
        # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('TwitchChat')

        # Print out some data about the table.
        # This will cause a request to be made to DynamoDB and its attribute
        # values will be set based on the response.
    print(table.creation_date_time)

    response = table.put_item(
       Item={
            'chat_id': chat_id,
            'message': message,
            'channel': channel,
            'timestamp': timestamp
        }
    )
    return response

    #TODO formatting and bulk pushing data to the database


if __name__ == '__main__':
    #chat_table = create_chat_table()
    #print("Table status:", chat_table.table_status)
    msg_resp = put_msg(123456789, "poggers",
                           "billybob", "2021-10-12 20:59:22.973000")
    print("Put msg succeeded:")
    pprint(msg_resp)