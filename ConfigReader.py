import json
import Logger

def loadConfig():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        Logger.logger.error(f"Ошибка: {e}")

