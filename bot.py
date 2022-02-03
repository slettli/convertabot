import os
import discord
import re
from dotenv import load_dotenv

import convert as c

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()

@client.event # Show initial connection
async def on_ready():
    print(f'{client.user} has connected!')

errorArr = ["Invalid number and unit", "Invalid number", "Invalid unit"]

@client.event # Message recognition and conversions
async def on_message(message):
    if message.author == client.user:
        return
    elif re.search(r'\d', message.content): # Try converting if number found, just to parse down all messages a bit
        await message.channel.send('Number recognized!')
        m = message.content
        response = c.convertHandler(m)
        if response in errorArr: # If invalid unit or number, print to console
            print(response)
        else: # Else send converted unit to channel
            await message.channel.send(response)

client.run(TOKEN)