import aiohttp
import asyncio
import Logger

async def SendMassage(token, ids, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": "",
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with aiohttp.ClientSession() as session:
            for id in ids:
                data["chat_id"] = id
                async with session.post(url, json=data) as answer:
                    if answer.status == 200:
                        Logger.logger.info(f"Сообщение отправлено: {id}")
                    else:
                        Logger.logger.error(f"Ошибка: {answer.status}")
    except Exception as e:
        Logger.logger.error(f"Ошибка: {e}")