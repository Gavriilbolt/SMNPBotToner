import Device
import GlobalInfo
import asyncio 
import TelegramSendAlert
import TelegramListener
import Logger
import BotUpdater

async def MainLoop():
    GlobalInfo.Info.printers = BotUpdater.InitPrinters()

    listenTask = TelegramListener.CommandListener(GlobalInfo.Info.tgToken, GlobalInfo.Info.tgIDs)
    async def PrinterChecker():
        while(True):
            tasks = []
            for printer in GlobalInfo.Info.printers:
                tasks.append(printer.CheckState())
            await asyncio.gather(*tasks)
            await asyncio.sleep(GlobalInfo.Info.timeCheck)

    checkTask = PrinterChecker()

    await asyncio.gather(listenTask, checkTask)
        
if __name__ == "__main__":
    #try:
        asyncio.run(MainLoop())
    #except Exception as e:
        #Logger.logger.error(f"Ошибка: {e}")
        #msg = f"<strong> Программа была завершена с ошибкой: </strong> {e}"
        #asyncio.run(TelegramSendAlert.SendMassage(GlobalInfo.Info.tgToken, GlobalInfo.Info.tgIDs, msg))


