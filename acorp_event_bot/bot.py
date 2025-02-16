import discord
from discord.ext import commands
from config import Config
import asyncio
from contextlib import nullcontext
import logging
import events

logger = logging.getLogger(__name__)

def start(config: Config) -> None:
    asyncio.run(start_bot(config))

async def start_bot(config: Config) -> None:
    intents = discord.Intents.none()
    intents.guild_scheduled_events = True
    intents.guilds = True 
    
    logger.info("Starting Bot")
    async with nullcontext() as google:
        # TODO replace nullcontext with whatever you use 
        async with AcorpBot(
                commands.when_mentioned,
                intents = intents,
                config=config,
                google=google
                ) as bot:
            await bot.start(config["discord"]["token"])

    


class AcorpBot(commands.Bot):
    def __init__(
        self,
        *args,
        config: dict,
        google,
        initial_extensions: list[str] = ["events"],
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.config = config
        self.google = google
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:

        for extension in self.initial_extensions:
            await self.load_extension(extension)

