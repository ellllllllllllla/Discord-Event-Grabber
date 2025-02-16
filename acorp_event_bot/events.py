import discord
from discord.ext import tasks, commands
import datetime

import logging
logger = logging.getLogger(__name__)

async def update_event(event: discord.ScheduledEvent):
    """ An event is added, updated, or removed.

    Use `event.status == discord.EventStatus.cancelled` to check if the event was deleted.
    ignore completed events to keep on calender?
    
    Some useful attributes:
    event.id: int           unique key
    event.name: str
    event.description: Optional[str]
    event.start_time: datatime.datetime
    event.end_time: Optional[datetime.datetime]
    event.creator: Optional[User]
    event.creator.display_name: str
    event.creator.global_name: str 
    event.cover_image: optional[Asset]
    event.cover_image.url: str
    

    `Asset` has some coroutines to save it locally if thats helpful.
    it might make more sense to use global_name than display_name if people are changing their
    server nicknames.

    """
    logger.info(f"Updating event {event.name} with id: {event.id}")
    # TODO

async def update_all_events(events: list[discord.ScheduledEvent]):
    """ An exhaustive list of all active events 
    
    Currently setup to run once a day
    
    

    """
    logger.info(f"Syncing all events")
    # TODO
    

async def setup(bot) -> None:
    """ Run when born """
    # TODO Add setup code to connect to google services here or add to cog up to you
    logger.info(f"Loading events extension")
    guilds = [await bot.fetch_guild(int(bot.config["events"]["guild"]))]
    await bot.add_cog(EventCog(bot, guilds))

async def teardown(bot) -> None:
    """ Run when murdered """
    logger.info(f"unloading events extension")
    await bot.remove_cog("EventCog")
    # TODO Add setup code to disconnect to google services here
    

class EventCog(commands.Cog):
    def __init__(self, bot, guilds):
        self.bot = bot
        self.config = bot.config
        
        self.guilds = guilds
        logger.info(f"{self.config["events"]["guild"]} {self.guilds[0]}")
        self.sync_events.start()

    def cog_unload(self):
        self.sync_events.cancel()

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event):
        await self.update_event(event)
    
    @commands.Cog.listener()
    async def on_scheduled_event_delete(self, event):
        await self.update_event(event)

    @commands.Cog.listener()
    async def on_scheduled_event_update(self, before, event):
        await self.update_event(event)
    
    async def update_event(self, event):
        if event.guild in self.guilds:
            await update_event(event)

    @tasks.loop(time=datetime.time(hour=12))
    async def sync_events(self):
        logger.info("Getting All Events")
        events = []
        for guild in self.guilds:
            events.extend(await guild.fetch_scheduled_events())
        await update_all_events(events)
        

    @sync_events.before_loop
    async def sync_events_wait_for_ready(self):
        await self.bot.wait_until_ready()
