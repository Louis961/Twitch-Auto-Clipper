f = open('log.txt', 'r', errors='ignore')

for line in f:
    content2 = line.split()

    sample = ''
    messageID = ''
    for char in content2[1]:
        if char != ']':
            sample += char
    messageID = sample[9:]
    print('MessageID: ' + messageID)

    datetime = ''
    for item in content2[0:2]:
        for char in item:
            if char != '[' and char != ']':
                datetime += char
        datetime += ' '
    print('Date and time: ' + datetime)

    user = ''
    for char in content2[2]:
        if char != ':':
            user += char
    print('User: ' + user)

    message = ''
    for item in content2[3:]:
        for char in item:
            message += char
        message += ' '
    print('Message: ' + message)

    print('\n')

f.close()
