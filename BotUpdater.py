import ConfigReader
import GlobalInfo
import Device
import Logger

def InitPrinters():
    printers = []
    for printer in GlobalInfo.Info.config["printers"]:
        printers.append(Device.Printer(printer["name"], printer["ip"], printer["cartridges"]))
    return printers


async def UpdateConfig():
    data = ConfigReader.loadConfig()
    GlobalInfo.Info.Update(data)
    GlobalInfo.Info.printers = InitPrinters()
    Logger.logger = Logger.CreateLogger()