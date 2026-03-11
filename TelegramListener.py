import aiohttp
import asyncio
import GlobalInfo
import Logger
import BotUpdater

async def CommandListener(token, ids):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    offset = 0

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                params = {"offset": offset, "time": 30}

                async with session.get(url, params=params) as answer:
                    if answer.status != 200:
                        await asyncio.sleep(5)
                        continue

                    data = await answer.json()

                    if not data["ok"] or not data["result"]:
                        continue

                    for update in data["result"]:
                        offset = update["update_id"] + 1

                        if "message" not in update:
                            continue
                        message = update["message"]
                        chatID = message["chat"]["id"]
                        text = message.get("text", "")

                        if chatID not in ids:
                            continue
                        if text == "/log":
                            Logger.logger.info(f"Запрос логов от {chatID}")
                            await sendFile(token, chatID)
                        elif text == "/toner":
                            Logger.logger.info(f"Запрос состояния принтеров от {chatID}")
                            msg = ""
                            for printer in GlobalInfo.Info.printers:
                                msg += printer.GetData()
                            await sendMessage(token, chatID, msg)
                        #elif text == "/update":
                            #await BotUpdater.UpdateConfig()
                            #await sendMessage(token, chatID, "Обновление успешно?")


            except Exception as e:
                Logger.logger.error(f"Ошибка: {e}")
                await asyncio.sleep(5)

async def sendFile(token, chatID):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    try:
        with open("bot.log", "rb") as f:
            data = aiohttp.FormData()
            data.add_field('chat_id', str(chatID))
            data.add_field('document', f, filename='bot_logs.txt')

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as answer:
                    if answer.status == 200:
                        Logger.logger.info("Логи успешно отправились")
                    else:
                        print(f"Логи не были отправлены: {answer.status}")
    except Exception as e:
        Logger.logger.error(f"Ошибка отправки при исключении: {e}")

async def sendMessage(token, chatID, msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chatID,
        "text": msg,
        "parse_mode": "HTML"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as answer:
                if answer.status == 200:
                    print(f"Отправка {chatID} успешна")
                else:
                    print(f"Ошибка отправки при {answer.status}")
    except Exception as e:
        Logger.logger.error(f"Ошибка отправки при исключении: {e}")


    
