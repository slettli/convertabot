import datetime
import os

import hikari
import lightbulb
from dotenv import load_dotenv

from convertabot.utils import convert as c


# Initial setup
class Bot(lightbulb.BotApp):

    def __init__(self) -> None:
        load_dotenv()
        super().__init__(token=os.getenv('DISCORD_TOKEN'),
                         intents=hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT))
        self.start_time: datetime.datetime = datetime.datetime.now()
        self.max_responses = 3
        self.load_extensions_from("convertabot/plugins/")  # Load commands


# Handles message parsing, calls relevant functions/modules. Returns formatted response
def parse_message(msg, maxResponses):
    response = c.convertHandler(msg, maxResponses)

    if not response or maxResponses < len(response):  # If no response found
        return

    fullResponse = ""  # Filter out and format successful conversions
    for r in response:
        if r:
            fullResponse += r + "\n"

    return fullResponse
