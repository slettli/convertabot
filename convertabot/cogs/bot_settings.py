import lightbulb

from convertabot.core.bot import Bot


@Bot.command()
@Bot.lightbulb.option("max", "Max number of conversions from one message, 1-10", int)
@Bot.lightbulb.command("set_max", "Set max number of conversions from one message, to avoid filling up chat")
@Bot.lightbulb.implements(lightbulb.SlashCommand)
async def set_max(ctx: lightbulb.Context) -> None:
    if ctx.options.max > 10 or ctx.options.max < 1:
        await ctx.respond("Please set a value between 1 and 10.")
    else:
        global MAX_RESPONSES
        MAX_RESPONSES = ctx.options.max
        await ctx.respond(f"The new conversions limit per message is now {MAX_RESPONSES}.")
