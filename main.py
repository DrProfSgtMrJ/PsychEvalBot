import os
import logging
from dotenv import load_dotenv
from discord import Intents
from discord.ext import commands

from cogs.psycheval import PsychEvalCog

load_dotenv()


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
DISCORD_LOG_FILE_NAME = os.getenv("DISCORD_LOG_FILE_NAME", "discord.log")
DISCORD_LOG_LEVEL = os.getenv("DISCORD_LOG_LEVEL", "DEBUG").upper()



logger_handler = logging.FileHandler(filename=DISCORD_LOG_FILE_NAME, encoding="utf-8", mode="w")
intents = Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

async def main():
    async with bot:
        await bot.add_cog(PsychEvalCog(bot))
        await bot.start(DISCORD_TOKEN)
        print("Bot started successfully.")

def setup_logging():
    match DISCORD_LOG_LEVEL:
        case "DEBUG":
            level = logging.DEBUG
        case "INFO":
            level = logging.INFO
        case "WARNING":
            level = logging.WARNING
        case "ERROR":
            level = logging.ERROR
        case "CRITICAL":
            level = logging.CRITICAL
        case _:
            level = logging.NOTSET

    logging.basicConfig(level=level, handlers=[logger_handler])


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info('------')
    logging.debug('Bot is ready to receive commands.')

if __name__ == "__main__":
    import asyncio
    setup_logging()
    asyncio.run(main())