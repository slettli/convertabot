import re

import hikari
import lightbulb

from convertabot.core.bot import Bot, parse_message


class Plugin(lightbulb.Plugin):
    def __init__(self) -> None:
        super().__init__("auto_convert listener")
        self.ignored = True
        self.bot: Bot


plugin = Plugin()


@plugin.listener(hikari.MessageCreateEvent)
async def auto_convert(ctx: hikari.MessageCreateEvent) -> None:
    if not ctx.is_human:
        return

    # Try converting only if number followed by letter found, to trim number of messages parsed
    if re.search(r"\d\s[A-Za-z]|\d[A-Za-z]", ctx.message.content):
        try:
            response = parse_message(ctx.message.content, plugin.bot.max_responses)

            if not response:
                return

            await plugin.bot.rest.create_message(ctx.channel_id, response, reply=ctx.message)
        except Exception as e:
            print(f"Exception: '{e}'\nWhile parsing: '{ctx.message.content}'\n")
            return


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
