import re

import hikari

from convertabot.core.bot import parseMessage, MAX_RESPONSES


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
