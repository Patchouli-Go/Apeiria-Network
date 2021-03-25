from nonebot.log import logger, default_filter
import sys

custom_format = "| \x1b[36mApeiria-Network\x1b[0m | <g>{time:MM-DD HH:mm:ss}</g> [<lvl>{level}</lvl>] <c><u>{name}</u></c> | {message}"
logger.remove()
logger.add(
    (sys.stdout),
    colorize=True,
    diagnose=False,
    filter=default_filter,
    format=custom_format,
)
