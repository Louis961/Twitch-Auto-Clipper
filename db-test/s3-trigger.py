import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

chatTable = dynamodb.Table('TwitchChat')
peakTable = dynamodb.Table('PeakFinder')

def FindRepeats(arr, required_number, num_repeats):
    idx = 0
    idxArr = []
    while idx < len(arr):
        if [required_number]*num_repeats == arr[idx:idx+num_repeats]:
            idxArr.append(idx)
            idx += num_repeats
        else:
            idx += 1
    return idxArr
    
def TimeStamps(timeArr, idxArr):
    stampArr = []
    for i in range(len(idxArr)):
        stampArr.append(timeArr[i])
        stampArr.append(timeArr[i+14])
    return stampArr

def lambda_handler(event, context):
    if event:
        # Read the uploaded S3 item into the python code
        file_obj = event['Records'][0]
        filename = str(file_obj['s3']['object']['key'])
        fileObj = s3.get_object(Bucket = "text-file", Key = filename)
        file_content = fileObj['Body'].read().decode('utf-8')
        
        with chatTable.batch_writer() as batch:
            # Start of actual coding
            dtArr = []
            timeArr = []
            secArr = []
            rateArr = []
            boolArr = []
            x = 0
            
            # Split the .txt file into list of separated messages
            content = file_content.split('\n')
            
            # Iterate through entire .txt file to grab necessary info
            for i in range(len(content)):
                # Iterate the indexed string to pull date/time info
                datetime = ''
                time = ''
                counter = 27
                for count, char in enumerate(content[i][1:counter]):
                    if char == ']':
                        counter = count + 1
                        break
                    datetime += char
                if len(datetime) < 25:
                    datetime += '.000000'
                content[i] = content[i].replace(content[i][0:counter+2], '')
                time = datetime[11:26]
                dtArr.append(datetime)
                if time:
                    timeArr.append(time)
    
                # Set to 16 because 15 is the max amount of characters in a Twitch username
                counter = 25
                for count, char in enumerate(content[i][0:counter]):
                    if char == ':':
                        counter = count + 1
                        break
                content[i] = content[i].replace(content[i][0:counter+1], '')
                
                # Iterate the rest of the list and make them the message string
                counter = 0
                for count, char in enumerate(content[i]):
                    counter = count
                content[i] = content[i].replace(content[i][0:counter+1], '')
                
                # At this point of the code, the content list taken from the .txt file should be empty
                
            # Algorithm uses time array to calculate rates and figure out peak times
            # Converting all recorded times to seconds
    
            for i in range(len(timeArr)):
                hour = float(timeArr[i][0:2])
                minute = float(timeArr[i][3:5])
                sec = float(timeArr[i][6:])
                totalSec = (hour * 60 * 60) + (minute * 60) + sec
                secArr.append(totalSec)
                x = x + 1
                
            # Code block uses the the seconds array to calculate the rate at which messages are coming in
            # Sort function error handles messages that were sent after a delay
            secArr.sort()
            for i in range(1, x):
                time2 = secArr[i] - secArr[i-1]
                rateArr.append(round(time2, 3))
                
            for i in range(len(rateArr)):
                if rateArr[i] < 0.1:
                    boolArr.append(True)
                else:
                    boolArr.append(False)
                    
            idxArr = FindRepeats(boolArr, True, 10)
            stampArr = TimeStamps(dtArr, idxArr)
            
            print(idxArr)
            print(stampArr)
            
            # TODO: PUTS PEAK CHAT ACTIVITY TIMESTAMPS INTO PEAKFINDER TABLE ON DDB
            y = 0
            for element1, element2 in zip(stampArr[0::2], stampArr[1::2]):
                peakTable.put_item(
                    Item = {
                        'startClip': element1,
                        'endClip': element2
                    }
                )
                y += 1
                
            print(y)
            print(x)
        
    return {'statusCode': 200, 'body': 'Done!'}
