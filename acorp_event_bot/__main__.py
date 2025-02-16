import config
import bot
import logging
logger = logging.getLogger(__name__)

config.setup_stream_logging()
logger.info("Hello World!")
CONFIG = config.load_config()
config.setup_file_logging(CONFIG)

bot.start(CONFIG)


