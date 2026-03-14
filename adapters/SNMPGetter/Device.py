from SNMPGetter import GetOIDInfo
from adapters.TelegramSendAlert import TelegramSendAlert
from kernels.GlobalInfo import GlobalInfo
import asyncio
from kernels.Logger import Logger


class Device:
    def __init__(self, name, IP):
        self.name = name
        self.ip = IP

class Printer(Device):
    def __init__(self, name, IP, Cartridges):
        '''
        Cartridges = 
        {
            "color":
            {
                "current": "OIDNow"
                "max": "OIDMax"
                "warning": "10"
            }
        }

        '''
        super().__init__(name, IP)
        self.Cartridges = Cartridges
        for color, item in self.Cartridges.items():
            item["status"] = 0
            item["isWarning"] = False

        self.isError = False

            

    async def CheckState(self):

        try:
            error, bind = await GetOIDInfo(self.ip, "1.3.6.1.2.1.1.5.0", True)
            if not self.isError and any(error):
                self.isError = True
                await TelegramSendAlert.SendMassage(GlobalInfo.Info.tgToken, GlobalInfo.Info.tgIDs, f"<b>ПРИНТЕР {self.name} ПОД {self.ip} ВЫЗЫВАЕТ ОШИБКИ</b> {error}")
            elif self.isError and not any(error):
                self.isError = False

            if self.isError : return
            
        except Exception as e:
            Logger.logger.error(f"Не удалось проверить состояние принтера, ошибки: {e}")

        tasks = []

        cartKeys = list(self.Cartridges.keys())

        for color in cartKeys:
            cart = self.Cartridges[color]
            tasks.append(self.CheckCartridge(color, cart))
            
        await asyncio.gather(*tasks)

        Logger.logger.info(self.GetData())
            #resultNow = asyncio.run(GetOIDInfo("127.0.0.1", ".1.3.6.1.2.1.43.11.1.1.9.1.2", False))
            #resultMax = asyncio.run(GetOIDInfo("127.0.0.1", ".1.3.6.1.2.1.43.11.1.1.8.1.2", False))
    async def CheckCartridge(self, color, cart):
        try:
            resultNow, resultMax = await asyncio.gather(GetOIDInfo(self.ip, cart["current"], False), GetOIDInfo(self.ip, cart["max"], False))
            resultNow = float(resultNow)
            resultMax = float(resultMax)


            if resultMax == 0: return

            prcnt = (resultNow) / (resultMax) * 100

            self.Cartridges[color]["status"] = prcnt

            warningLevel = int(cart["warning"])

            if (prcnt <= warningLevel and not cart["isWarning"]):

                cart["isWarning"] = True

                massage = GlobalInfo.Info.massage
                massage = massage.replace("{NAME}", f"{self.name}").replace("{COLOR}", cart["color"]).replace("{IP}", f"{self.ip}").replace("{PRCNT}", f"{prcnt:.2f}")

                await TelegramSendAlert.SendMassage(GlobalInfo.Info.tgToken, GlobalInfo.Info.tgIDs, massage)

                return 0

            elif (prcnt > int(cart["warning"]) and cart["isWarning"]):

                cart["isWarning"] = False

                return 1

        except Exception as e:

                Logger.logger.error(("ОШИБКА РАСЧЁТА У " + cart["color"], f"в принтере {self.name} под адрессом {self.ip} | " f"{e}, возможно нет соеденения с устройством или неверный OID"))            

    def GetData(self):
        carts = []
        for color in list(self.Cartridges.keys()):
            carts.append(self.Cartridges[color])
        #Logger.logger.info(("="*10, self.name, "="*10))
        cartsMsg = ""
        for cart in carts:
            cartsMsg += f"{cart['color']} : {cart['status']:.2f} | {int(cart['warning'])}\n"
        finalMsg = (
            f"\n {'='*10}{self.name}{'='*10}\n" +
            cartsMsg +
            f"{'-'*30}"
        )
        return finalMsg
            #Logger.logger.info((cart["color"] + ":", f"{cart['status']:.2f}",  " | ", int(cart["warning"])))
        #Logger.logger.info("-"*30)