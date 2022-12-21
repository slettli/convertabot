import os
import datetime
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
start_time: datetime.datetime = datetime.datetime.now()

@bot.listen()
async def auto_convert(ctx: hikari.MessageCreateEvent) -> None: # Auto parse messages sent in servers
    if not ctx.is_human:
        return
        
    if re.search(r'\d', ctx.message.content): # Try converting if number found, just to trim number of messages a bit
        try:
            response = parseMessage(ctx.message.content,MAX_RESPONSES)
            #print('Number recognized! - ' + ctx.message.content)           
            if len(response) == 0: # If conversion failed
                return 
            await bot.rest.create_message(ctx.channel_id, response)
           # print(response)
        except Exception as e:
            print(f"Exception: '{e}'\nWhile parsing: '{ctx.message.content}'\n")
            return

# Check if the bot is online, or just waste computing resources.
@bot.command()
@lightbulb.command("poke", "Poke Covertabot.")
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

# Check if the bot is online, or just waste computing resources.
@bot.command()
@lightbulb.option("max", "Max number of conversions from one message", int)
@lightbulb.command("set_max", "Set max number of conversions from one message, to avoid filling chat.")
@lightbulb.implements(lightbulb.SlashCommand)
async def poke(ctx: lightbulb.Context) -> None: 
    global MAX_RESPONSES
    MAX_RESPONSES = ctx.options.max
    await ctx.respond(f"The new conversions limit per message is now {MAX_RESPONSES}!")

# Same as the auto parser. Will attempt to convert measurements imperial->metric or vice versa.
@bot.command()
@lightbulb.option("value", "Value to convert, use . for decimal notation", float)
@lightbulb.option("unit", "Unit to convert from", str)
@lightbulb.command("convert", "Convert a measurement to whatever Convertabot thinks is best", aliases=["autocon","autoconvert"])
@lightbulb.implements(lightbulb.SlashCommand)
async def convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit
    comb = str(number) + unit
    result = parseMessage(comb, 1)
    await ctx.respond(result)

# Convert from one unit to another one, of the user's choosing.
@bot.command()
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
