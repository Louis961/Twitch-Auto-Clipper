import boto3

def create_chat_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='TwitchChat',
        KeySchema=[
            {
                'AttributeName': 'chat_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'channel',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'N'
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
    return table


if __name__ == '__main__':
    chat_table = create_chat_table()
    print("Table status:", chat_table.table_status)