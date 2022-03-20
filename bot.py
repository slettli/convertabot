from ast import excepthandler
import os
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands

import convert as c

load_dotenv()
TOKEN = os.getenv('TOKEN')

MAX_RESPONSES = 3 # Max num of conversions the bot will do from a single message, to avoid filling up chat

#client = discord.Client()
client = commands.Bot(command_prefix="!", help_command=None, status=discord.Status.idle)

@client.event # Show initial connection
async def on_ready():
    print(f'{client.user} is now online!\n')

errorArr = ["Invalid number and unit", "Invalid number", "Invalid unit"]

class Utility_Commands(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command()
    async def paywall(self,ctx, arg=None):
        if arg==None:
            await ctx.channel.send("Did you forget the link?")
        else:
            await ctx.channel.send(f"Heckin frick paywalls: https://12ft.io/{arg}")

    @commands.command()
    async def unwall(self,ctx, arg):
        if arg==None:
            await ctx.channel.send("Did you forget the link?")
        else:
            await ctx.channel.send(f"Heckin frick paywalls: https://12ft.io/{arg}")

    @commands.command()
    async def ladder(self,ctx, arg):
        if arg==None:
            await ctx.channel.send("Did you forget the link?")
        else:
            await ctx.channel.send(f"Heckin frick paywalls: https://12ft.io/{arg}")
    

class Automatic_Converter(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == client.user or ctx.author.bot == True:
            return
        elif ctx.content in (['!paywall','!unwall','ladder'] ):
            return
        elif ctx.content == "$vaffel": # Joke command as an inside joke 
            await ctx.channel.send("Vi har ikke åpnet for bestillinger.")
        elif re.search(r'\d', ctx.content): # Try converting if number found, just to trim number of messages a bit
            try:
                response = parseMessage(ctx,MAX_RESPONSES)
                print('Number recognized! - ' + ctx.content)           
                if len(response) == 0:
                    return 
                await ctx.channel.send(response)
                print(response)
            except Exception as e:
                print(f"Exception: '{e}'\nWhile parsing: '{ctx.content}'\n")
                return

# Handles message parsing, calls relevant functions/modules. Returns formatted response
def parseMessage(message, maxResponses):
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

client.add_cog(Utility_Commands(client))
client.add_cog(Automatic_Converter(client))
client.run(TOKEN)

'''
TODO features to be added
- Make it handle messages that couldn't be parsed in a graceful manner (don't fill up the terminal with errors)
- Treat , as . (but only if not mixed)
- Add km/h and mp/h
- Add dl, ml, ounce (oz)
- Add verbose mode
- A foot, an inch, a meter etc

    - Also focus on school

After above implemented, stop for a bit and focus on making experience better.
    - Like commands
    - Don't worry about new units for a while


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