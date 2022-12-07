import json


class Config():
    __linkConfig = "CONFIG.txt"

    def setConfig(self, configData):
        with open(self.__linkConfig, "w") as CONFIG:
            json.dump(configData, CONFIG)

    def getConfig(self):
        with open(self.__linkConfig) as CONFIG:
            return json.load(CONFIG)
