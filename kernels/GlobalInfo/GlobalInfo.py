import ConfigReader
class GlobalInfo:
    def __init__(self, config):
        self.config = config
        self.log = bool(self.config["log"])
        self.extLog = bool(self.config["extendedLog"])
        self.massage = self.config["telegram_massage"]
        self.tgToken = self.config["telegram_token"]
        self.tgIDs = self.config["telegram_IDs"]
        self.timeCheck = self.config["check_interval"]
        self.printers = None
    def Update(self, config):
        self.__init__(config)
Info = GlobalInfo(ConfigReader.loadConfig())
