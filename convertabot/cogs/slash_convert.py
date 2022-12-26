import lightbulb

from convertabot.core.bot import Bot, parseMessage


@Bot.command()
@Bot.lightbulb.option("value", "Value to convert (use . for decimal notation)", float)
@Bot.lightbulb.option("unit", "Unit to convert from", str)
@Bot.lightbulb.command("convert", "Convert a measurement to whatever June thinks is best", aliases=["autocon","autoconvert"])
@Bot.lightbulb.implements(lightbulb.SlashCommand)
async def convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit
    comb = str(number) + unit
    result = parseMessage(comb, 1)
    await ctx.respond(result)


@Bot.command()
@Bot.lightbulb.option("value", "Value to convert (use . for decimal notation)", float)
@Bot.lightbulb.option("unit_1", "Unit to convert from", str)
@Bot.lightbulb.option("unit_2", "Target unit", str)
@Bot.lightbulb.command("manual_convert", "Convert from one unit to another (if possible)", aliases=["mancon","manualcon"])
@Bot.lightbulb.implements(lightbulb.SlashCommand)
async def manual_convert(ctx: lightbulb.Context) -> None:
    number = ctx.options.value
    unit = ctx.options.unit_1
    target_unit = ctx.options.unit_2
    comb = str(number) + unit
    result = parseMessage(comb, 1)
    await ctx.respond(result)
