import os
import datetime
import hikari
import lightbulb
import re
from dotenv import load_dotenv

import convert as c

MAX_RESPONSES = 3 # Default max num of conversions the bot will do from a single message, to avoid filling up chat

# Initial setup
load_dotenv()
token = os.getenv('TOKEN')
bot = lightbulb.BotApp(token, intents = hikari.Intents(hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.MESSAGE_CONTENT))
start_time: datetime.datetime = datetime.datetime.now()

# Parse incoming messages if auto-conversion enabled
@bot.listen()
async def auto_convert(ctx: hikari.MessageCreateEvent) -> None: # Auto parse messages sent in servers
    if not ctx.is_human:
        return 
        
    if re.search(r'\d', ctx.message.content): # Try converting if number found, just to trim number of messages a bit
        try:
            response = parseMessage(ctx.message.content , MAX_RESPONSES)

            if not response:
                return

            await bot.rest.create_message(ctx.channel_id, response)
        except Exception as e:
            print(f"Exception: '{e}'\nWhile parsing: '{ctx.message.content}'\n")
            return

# Commands

# Check if the bot is online, or just waste computing resources.
@bot.command()
@lightbulb.command("poke", "Poke June.")
@lightbulb.implements(lightbulb.SlashCommand)
async def poke(ctx: lightbulb.Context) -> None: 
    await ctx.respond("Stop that!")

# Uptime for the bot.
@bot.command()
@lightbulb.command("uptime", "Time since last crash.")
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
@lightbulb.option("max", "Max number of conversions from one message, 1-20", int)
@lightbulb.command("set_max", "Set max number of conversions from one message, to avoid filling chat.")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_max(ctx: lightbulb.Context) -> None: 
    if ctx.options.max > 10 or ctx.options.max < 1:
        await ctx.respond("Please set a value between 1 and 20.")
    else:
        global MAX_RESPONSES
        MAX_RESPONSES = ctx.options.max
        await ctx.respond(f"The new conversions limit per message is now {MAX_RESPONSES}.")

# Same as the auto parser. Will attempt to convert measurements imperial -> metric or vice versa.
@bot.command()
@lightbulb.option("value", "Value to convert, use . for decimal notation", float)
@lightbulb.option("unit", "Unit to convert from", str)
@lightbulb.command("convert", "Convert a measurement to whatever June thinks is best", aliases=["autocon","autoconvert"])
@lightbulb.implements(lightbulb.SlashCommand)
async def convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit
    comb = str(number) + unit
    result = parseMessage(comb, 1)
    await ctx.respond(result)

# Convert one unit to another unit, user's choice.
#@bot.command()
@lightbulb.option("value", "Value to convert, use . for decimal notation", float)
@lightbulb.option("unit_1", "Unit to convert FROM", str)
@lightbulb.option("unit_2", "Final unit after conversion", str)
@lightbulb.command("manualconvert", "Convert from one unit to another.", aliases=["mancon","manualcon"])
@lightbulb.implements(lightbulb.SlashCommand)
async def manualconvert(ctx: lightbulb.Context) -> None:
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
