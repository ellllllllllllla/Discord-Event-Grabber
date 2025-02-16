import toml
import sys
import discord
import datetime
from pathlib import Path
from discord.utils import _ColourFormatter, stream_supports_colour

import logging
logger = logging.getLogger(__name__)

type Config = dict

default_config = """
# ACORP Event Bot

[discord]
token = ""

[logging]
level = 20 # INFO
log_to_file = true
path = "./logs/"

[events]
guild = 1159391121999413310

"""



def load_config() -> Config:
    logger.info("Loading config")
    try:
        with open("config.toml", "r") as file:
            unparsed_config = file.read()
    except FileNotFoundError:
        logger.critical("No config file, Creating...")
        with open("config.toml", "x") as file:
            file.write(default_config)
        logger.critical("Please set config, Exiting...")
        sys.exit()
    return toml.loads(unparsed_config)

def setup_stream_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    if isinstance(handler, logging.StreamHandler) and stream_supports_colour(handler.stream):
        formatter = _ColourFormatter()
    else:
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(
                "[{asctime}] [{levelname:<8}] {name}: {message}", 
                dt_fmt, 
                style="{"
                        )
                # } <- the opening brace is messing with my formatter >.<

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

def setup_file_logging(config: Config) -> None:
    root_logger = logging.getLogger()
    try:
        root_logger.setLevel(config["logging"]["level"])
    except KeyError:
        pass
    if config["logging"]["log_to_file"]:
        Path(config["logging"]["path"]).mkdir(parents=True, exist_ok=True)
        filename = config["logging"]["path"] + str(datetime.datetime.now())
        handler = logging.FileHandler(filename=filename)
        root_logger.addHandler(handler)
