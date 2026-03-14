import asyncio
from adapters.TelegramSendAlert import TelegramListener
from kernels.GlobalInfo import BotUpdater, GlobalInfo


async def MainLoopLogic():
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
        
def MainLoop():
    asyncio.run(MainLoopLogic())

