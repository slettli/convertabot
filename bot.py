import os
import hikari
import lightbulb
import re
from dotenv import load_dotenv

import convert as c

load_dotenv()
#TOKEN = os.getenv('TOKEN') # Live convertabot
TOKEN = os.getenv('TESTTOKEN') # Converta testbot

MAX_RESPONSES = 3 # Max num of conversions the bot will do from a single message, to avoid filling up chat

client = hikari.GatewayBot(token=TOKEN)

errorArr = ["Invalid number and unit", "Invalid number", "Invalid unit"]

class Automatic_Converter(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == bot.user or ctx.author.bot == True:
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

bot.add_cog(Automatic_Converter(bot))
bot.run(TOKEN)
