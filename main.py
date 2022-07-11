import os

import asyncio
import discord
from discord.ext import interaction

from config.config import get_config
from config.log_config import log

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    parser = get_config()

    log.info("몬티홀의 역설을 불러오는 중입니다.")
    if parser.getboolean("DEFAULT", "AutoShard"):
        log.info("Config 파일에서 AutoShard가 켜져있습니다. AutoShard 기능을 킵니다.")

        bot = interaction.AutoShardedClient(
            intents=discord.Intents.default(),
            enable_debug_events=True,
            global_sync_command=True,
        )
    else:
        bot = interaction.Client(
            intents=discord.Intents.default(),
            enable_debug_events=True,
            global_sync_command=True,
        )
    token = parser.get("DEFAULT", "token")
    # cogs = ["cogs." + file[:-3] for file in os.listdir(os.path.join(directory, 'cogs')) if file.endswith(".py")]
    # for cog in cogs:
    #    bot.load_extension(cog)

    asyncio.run(
        bot.load_extensions('cogs', directory)
    )
    bot.run(token=token)
