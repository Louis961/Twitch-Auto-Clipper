import os
from twitchio.ext import commands
import asyncio
import requests
from dotenv import load_dotenv
import boto3
import uuid

load_dotenv()

log = open("log.txt", "a")

with open('streamers.txt') as f:
    channels = f.read().splitlines()
    print(channels)


bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[]
)



def put_msg(message):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('chat_messages')

    response = table.put_item(
        Item={
            'chat_id': message['chat_id'],
            'content': message['content'],
            'channel': message['channel'],
            'timestamp': message['timestamp'],
            'author': message['author']
        }
    )
    #print(response)



@bot.event
async def event_ready():
    print(f"{os.environ['BOT_NICK']} is online!")
    count = 0
    for x in channels:
        print(f"Trying to join {x}")
        count+=1
        try:
            await bot.join_channels([x])
        except Exception as e:
            print(e)
        if count == 49:
            print("Sleeping...")
            await asyncio.sleep(15)
            count = 0

@bot.event
async def event_message(ctx):
    message = f"[{ctx.timestamp}] {ctx.author.display_name}: {ctx.content}\n"
    print(message)
    log.write(message)
    log.flush()

    dict_message = {
        'chat_id': str(uuid.uuid4()),
        'timestamp': str(ctx.timestamp),
        'author': ctx.author.display_name,
        'channel': str(ctx.channel),
        'content': ctx.content
    }

    put_msg(dict_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())
    loop.run_forever()
    #bot.run()
