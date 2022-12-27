import lightbulb

from convertabot.core.bot import parse_message

plugin = lightbulb.Plugin("slash_convert")


@plugin.command()
@lightbulb.option("value", "Value to convert (use . for decimal notation)", float)
@lightbulb.option("unit", "Unit to convert from", str)
@lightbulb.command("convert", "Convert a measurement to whatever June thinks is best",
                   aliases=["autocon", "autoconvert"])
@lightbulb.implements(lightbulb.SlashCommand)
async def convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit
    comb = str(number) + unit
    result = parse_message(comb, 1)
    await ctx.respond(result)


# @plugin.command()
@lightbulb.option("value", "Value to convert (use . for decimal notation)", float)
@lightbulb.option("unit_1", "Unit to convert from", str)
@lightbulb.option("unit_2", "Target unit", str)
@lightbulb.command("manual_convert", "Convert from one unit to another (if possible)", aliases=["mancon", "manualcon"])
@lightbulb.implements(lightbulb.SlashCommand)
async def manual_convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit_1
    target_unit = ctx.options.unit_2
    comb = str(number) + unit
    result = parse_message(comb, 1)
    await ctx.respond(result)


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
