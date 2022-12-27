import os

from core.bot import Bot

if __name__ == "__main__":
    bot = Bot()
    if os.name != "nt":
        import uvloop

        uvloop.install()

bot.run()
