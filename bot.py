import os
import discord
import re
from dotenv import load_dotenv

import convert as c

load_dotenv()
TOKEN = os.getenv('TOKEN')

MAX_RESPONSES = 3

client = discord.Client()

@client.event # Show initial connection
async def on_ready():
    print(f'{client.user} is now online!\n')

errorArr = ["Invalid number and unit", "Invalid number", "Invalid unit"]

@client.event # Message recognition and conversions
async def on_message(message):
    if message.author == client.user or message.author.bot == True:
        return
    elif re.search(r'\d', message.content): # Try converting if number found, just to parse down all messages a bit
        print('Number recognized! - ' + message.content)
        response = await parseMessage(message,MAX_RESPONSES)
        if len(response) == 0:
            return 

        await message.channel.send(response)
        print(response)

# Handles message parsing, calls relevant functions/modules. Returns formatted response
async def parseMessage(message,maxResponses):
    response = c.convertHandler(message.content,maxResponses)
    if len(response) == 0:
        return response
    fullResponse = ""
    for r in response:
        if r in errorArr: # If invalid unit or number, print to console
            pass
        else: # Else send converted responses to channel
            fullResponse += r + "\n"
    return fullResponse
        
client.run(TOKEN)

'''
TODO
- Treat , as .
- Add km/h and mp/h
- Support for negative temperatures
- Check that other message is not from a bot (to avoid infinite loops)

Long term:
- Add $converta og / commands
    - Help
        - Shows commands, short explanation of functionality
    - Units
        - Lists supported units
    - Volumenheter
    - Saved server configs
        - Required for below options
    - Toggle automatic mode on/off
        - Må først bruke command prefix by default
        - Toggle categories of units on/off
            - I.e. bare automatisk convertere lengde, mål, vekt, volum, temp
            - Må dele opp listene etter kategori.
            - Alle categories og mertic <--> imperial fungerer om man bruker prefix doe
        - Toggle only metric > imperial og omvendt, but both ways enabled by default
            - Alle categories og mertic <--> imperial fungerer om man bruker prefix doe
    - No "fun" messages ffs. Functionality over meme factor
    - T-Timezones...? Way fucking last if so
'''