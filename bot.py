import os
import hikari
import lightbulb
import re
from dotenv import load_dotenv

import convert as c

MAX_RESPONSES = 3 # Max num of conversions the bot will do from a single message, to avoid filling up chat

errorArr = ["Invalid number and unit", "Invalid number", "Invalid unit"]

load_dotenv()
token = os.getenv('TOKEN') # Converta testbot
bot = lightbulb.BotApp(token, intents = hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT))

@bot.listen()
async def auto_convert(ctx: hikari.MessageCreateEvent) -> None: # Auto parse messages sent in servers
    if not ctx.is_human:
        return
        
    if re.search(r'\d', ctx.message.content): # Try converting if number found, just to trim number of messages a bit
        try:
            response = parseMessage(ctx.message.content,MAX_RESPONSES)
            print('Number recognized! - ' + ctx.message.content)           
            if len(response) == 0:
                return 
            await bot.rest.create_message(ctx.channel_id, response)
            print(response)
        except Exception as e:
            print(f"Exception: '{e}'\nWhile parsing: '{ctx.message.content}'\n")
            return

# Handles message parsing, calls relevant functions/modules. Returns formatted response
def parseMessage(msg, maxResponses):
    response = c.convertHandler(msg,maxResponses)
    if len(response) == 0:
        return response        
    fullResponse = ""
    for r in response:
        if r in errorArr: # If invalid unit or number, print to console
            pass
        else: # Else send converted responses to channel
            fullResponse += r + "\n"
    return fullResponse

bot.run()
