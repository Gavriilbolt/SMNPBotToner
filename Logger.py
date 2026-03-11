import logging
import GlobalInfo
from logging.handlers import RotatingFileHandler

def CreateLogger():
    logger = logging.getLogger("TonerBot")
    logger.setLevel(logging.INFO)

    formatt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatt)
    logger.addHandler(consoleHandler)

    fileHandler = RotatingFileHandler("bot.log", maxBytes=1024*1024, backupCount=2, encoding="utf-8")
    fileHandler.setFormatter(formatt)
    logger.addHandler(fileHandler)
    return logger

logger = CreateLogger()
logger.disabled = not GlobalInfo.Info.log