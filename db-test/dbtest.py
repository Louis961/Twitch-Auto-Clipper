import boto3
from pprint import pprint


def find_repeats(arr, required_number, num_repeats):
    idx = 0
    idxArr = []
    while idx < len(arr):
        if [required_number]*num_repeats == arr[idx:idx+num_repeats]:
            idxArr.append(idx)
            idx += num_repeats
        else:
            idx += 1
    return idxArr

def put_msg(dynamodb=None):
    if not dynamodb:
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        # , endpoint_url="http://localhost:8000")
        # , region_name='us-east-1')

        # Instantiate a table resource object without actually
        # creating a DynamoDB table. Note that the attributes of this table
        # are lazy-loaded: a request is not made nor are the attribute
        # values populated until the attributes
        # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table('TwitchChat')

    # Print out some data about the table.
    # This will cause a request to be made to DynamoDB and its attribute
    # values will be set based on the response.
    # print(table.creation_date_time)
    f = open('log.txt', 'r', errors='ignore')
    with table.batch_writer() as batch:
        timeArr = []
        secArr = []
        rateArr = []
        count = 0
        for line in f:
            content = line.split()

            sample = ''
            messageID = ''
            for char in content[1]:
                if char != ']':
                    sample += char
            messageID = sample[9:]
            if messageID != '':
                messageID = int(messageID)
            #print('messageID: ' + messageID)

            datetime = ''
            for item in content[0:2]:
                for char in item:
                    if char != '[' and char != ']':
                        datetime += char
                datetime += ' '
            datetime = datetime[:-1]
            if len(datetime) < 25:
                datetime += '.000000'
            #print('Date and time: ' + datetime)
            timeArr.append(datetime)

            user = ''
            for char in content[2]:
                if char != ':':
                    user += char
            #print('User: ' + user)

            message = ''
            for item in content[3:]:
                for char in item:
                    message += char
                message += ' '
            #print('Message: ' + message)

            # print('\n')
            #if messageID == '':
            #    break
            #else:
            response = batch.put_item(
                Item={
                    'messageID': messageID,
                    'message': message,
                    'user': user,
                    'datetime': datetime
                }
            )
            # Algorithm for finding rates and peak finder
            time = ''
            for item in content[1]:
                for char in item:
                    if char != ']':
                        time += char
            hour = float(time[0:2])
            # Convert hours to seconds
            totalSec = hour * 60 * 60

            min = float(time[3:5])
            # Convert min to seconds
            totalSec = totalSec + min * 60

            sec = float(time[6:])
            totalSec = totalSec + sec
            secArr.append(totalSec)
            count = count + 1

            #print('\n')

        secArr.sort()
        time2 = 0.0
        for i in range(1, count):
            time2 = (secArr[i] - secArr[i-1]) / 2
            rateArr.append(round(time2, 2))

        boolArr = []
        for i in range(len(rateArr)):
            if rateArr[i] < 0.05:
                boolArr.append(True)
            else:
                boolArr.append(False)

        # Peak chat activity is based off of 10 consecutive chats that were sent consecutively
        # in less than 0.05 seconds within each one
        print("Timestamps of peak chat activity:")
        for i in (find_repeats(boolArr, True, 10)):
            print(timeArr[i] + " - " + timeArr[i+14])

        totalTime = secArr[-1] - secArr[0]
        totalRate = count / totalTime
        print("Total rate: " + str(round(totalRate, 2)) + " messages/sec")

    f.close()
    return response


if __name__ == '__main__':
    #chat_table = create_chat_table()
    #print("Table status:", chat_table.table_status)

    msg_resp = put_msg()

    print("Put msg succeeded:")
    pprint(msg_resp)
