import datetime

import lightbulb

from convertabot.core.bot import Bot


@Bot.command()
@Bot.lightbulb.command("poke", "Poke June")
@Bot.lightbulb.implements(lightbulb.SlashCommand)
async def poke(ctx: lightbulb.Context) -> None:
    await ctx.respond("Stop that!")


@Bot.command()
@Bot.lightbulb.command("uptime", "Time since last crash")
@Bot.lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx: lightbulb.Context) -> None:
    dt = datetime.datetime.now() - start_time
    dt -= datetime.timedelta(microseconds=dt.microseconds)
    if (dt.days > 0):
        await ctx.respond(f"`{str(dt)}` (days, hours, minutes, seconds)")
    else:
        await ctx.respond(f"`{str(dt)}` (hours, minutes, seconds)")
