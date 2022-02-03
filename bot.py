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
        print('Number recognized! - ' + message.content)
        response = c.convertHandler(message.content)
        if len(response) == 0:
            return 
        fullResponse = ""
        for r in response:
            if r in errorArr: # If invalid unit or number, print to console
                pass
            else: # Else send converted responses to channel
                fullResponse += r + "\n"
        print(fullResponse)
        await message.channel.send(fullResponse)
client.run(TOKEN)

'''
TODO
- Treat , as .
- Add km/h and mp/h
- Support for negative temperatures
'''