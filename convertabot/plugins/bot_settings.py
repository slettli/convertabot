import lightbulb

from convertabot.core.bot import Bot


class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__(name="bot_settings")
        self.bot: Bot


plugin = Plugin()


@plugin.command()
@lightbulb.option("max", "Max number of conversions from one message, 1-10", int)
@lightbulb.command("set_max", "Set max number of conversions from one message, to avoid filling up chat")
@lightbulb.implements(lightbulb.SlashCommand)
async def set_max(ctx: lightbulb.Context) -> None:
    if ctx.options.max > 10 or ctx.options.max < 1:
        await ctx.respond("Please set a value between 1 and 10.")
    else:
        plugin.bot.max_responses = ctx.options.max
        await ctx.respond(f"The new conversions limit per message is now {plugin.bot.max_responses}.")


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
