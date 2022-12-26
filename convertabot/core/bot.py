import datetime
import os
import re

import hikari
import lightbulb
from dotenv import load_dotenv

from convertabot.plugins import convert as c

MAX_RESPONSES = 3 # Default max num of conversions the bot will do from a single message, to avoid filling up chat

# Initial setup

class Bot(lightbulb.BotApp):

    def __init__(self) -> None:
        load_dotenv()
        lightbulb.BotApp(token=os.getenv('TOKEN'),
                         intents=hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT))
        start_time: datetime.datetime = datetime.datetime.now()

# Parse incoming messages if auto-conversion is enabled
@bot.listen()
async def auto_convert(ctx: hikari.MessageCreateEvent) -> None:
    if not ctx.is_human:
        return 

    # Try converting only if number followed by letter found, to trim number of messages parsed
    if re.search(r"\d\s[A-Za-z]|\d[A-Za-z]", ctx.message.content): 
        try:
            response = parseMessage(ctx.message.content , MAX_RESPONSES)

            if not response:
                return

            await bot.rest.create_message(ctx.channel_id, response, reply = ctx.message)
        except Exception as e:
            print(f"Exception: '{e}'\nWhile parsing: '{ctx.message.content}'\n")
            return

# Slash Commands

# Check if the bot is online, or just waste computing resources.
@bot.command()
@lightbulb.command("poke", "Poke June")
@lightbulb.implements(lightbulb.SlashCommand)
async def poke(ctx: lightbulb.Context) -> None: 
    await ctx.respond("Stop that!")

# Uptime for the bot.
@bot.command()
@lightbulb.command("uptime", "Time since last crash")
@lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx: lightbulb.Context) -> None: 
    dt = datetime.datetime.now() - start_time
    dt -= datetime.timedelta(microseconds=dt.microseconds)
    if (dt.days > 0):
        await ctx.respond(f"`{str(dt)}` (days, hours, minutes, seconds)")
    else:
        await ctx.respond(f"`{str(dt)}` (hours, minutes, seconds)")

# Set a max number of conversions from a single message
@bot.command()
@lightbulb.option("max", "Max number of conversions from one message, 1-10", int)
@lightbulb.command("set_max", "Set max number of conversions from one message, to avoid filling up chat")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_max(ctx: lightbulb.Context) -> None: 
    if ctx.options.max > 10 or ctx.options.max < 1:
        await ctx.respond("Please set a value between 1 and 10.")
    else:
        global MAX_RESPONSES
        MAX_RESPONSES = ctx.options.max
        await ctx.respond(f"The new conversions limit per message is now {MAX_RESPONSES}.")

# Same as the auto parser. Will attempt to convert measurements between imperial <-> metric.
@bot.command()
@lightbulb.option("value", "Value to convert (use . for decimal notation)", float)
@lightbulb.option("unit", "Unit to convert from", str)
@lightbulb.command("convert", "Convert a measurement to whatever June thinks is best", aliases=["autocon","autoconvert"])
@lightbulb.implements(lightbulb.SlashCommand)
async def convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit
    comb = str(number) + unit
    result = parseMessage(comb, 1)
    await ctx.respond(result)

# Convert one unit to another unit, user's choice. Not enabled or completed.
#@bot.command()
@lightbulb.option("value", "Value to convert (use . for decimal notation)", float)
@lightbulb.option("unit_1", "Unit to convert from", str)
@lightbulb.option("unit_2", "Target unit", str)
@lightbulb.command("manual_convert", "Convert from one unit to another (if possible)", aliases=["mancon","manualcon"])
@lightbulb.implements(lightbulb.SlashCommand)
async def manual_convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit_1
    target_unit = ctx.options.unit_2
    comb = str(number) + unit
    result = parseMessage(comb, 1)
    await ctx.respond(result)

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

bot.run()
