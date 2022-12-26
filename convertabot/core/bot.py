import datetime
import os

import hikari
import lightbulb
from dotenv import load_dotenv

from convertabot.plugins import convert as c

MAX_RESPONSES = 3 # Default max num of conversions the bot will do from a single message, to avoid filling up chat

# Initial setup

class Bot (lightbulb.BotApp):

    def __init__(self) -> None:
        load_dotenv()
        lightbulb.BotApp(token=os.getenv('TOKEN'),
                         intents=hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT))
        start_time: datetime.datetime = datetime.datetime.now()
        self.load_extensions_from("cogs")  # Load commands


# Handles message parsing, calls relevant functions/modules. Returns formatted response
def parseMessage(msg, maxResponses):
    response = c.convertHandler(msg,maxResponses)

    if not response: # If no response found
        return

    fullResponse = "" # Filter out and format successful conversions
    for r in response:
        if r:
            fullResponse += r + "\n"

    return fullResponse

bot = Bot()
bot.run()