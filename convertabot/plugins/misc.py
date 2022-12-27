import datetime

import lightbulb

from convertabot.core.bot import Bot


class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__(name="misc")
        self.bot: Bot


plugin = Plugin()


@plugin.command()
@lightbulb.command("poke", "Poke June")
@lightbulb.implements(lightbulb.SlashCommand)
async def poke(ctx: lightbulb.Context) -> None:
    await ctx.respond("Stop that!")


@plugin.command()
@lightbulb.command("uptime", "Time since last crash")
@lightbulb.implements(lightbulb.SlashCommand)
async def uptime(ctx: lightbulb.Context) -> None:
    dt = datetime.datetime.now() - plugin.bot.start_time
    dt -= datetime.timedelta(microseconds=dt.microseconds)
    if (dt.days > 0):
        await ctx.respond(f"`{str(dt)}` (days, hours, minutes, seconds)")
    else:
        await ctx.respond(f"`{str(dt)}` (hours, minutes, seconds)")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
