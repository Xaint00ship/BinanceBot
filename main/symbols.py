import requests
import json


class Symbols():
    __UrlSpot = open('URLSpot.txt', 'r').read()
    __UrlFutures = open('URLFutures.txt', 'r').read()

    def getRealPriceAllSymbol(self, typeExchange):
        if typeExchange == "spot":
            response = requests.get(self.__UrlSpot)
        else:
            response = requests.get(self.__UrlFutures)

        try:
            if response.status_code == 200:
                allPriceSymbol = json.loads(response.text)
                print(
                    f"Connection successful, status code: {response.status_code}")
                return allPriceSymbol
            else:
                raise ConnectionError

        except ConnectionError:
            print(f"Error, status code:{response.status_code}")
            print(ConnectionError)
            return []

    def getBasePriceAllSymbol(self, typeExchange):
        with open(f"baseValues{typeExchange}.json") as json_file:
            baseValues = json.load(json_file)
            return baseValues

    def setBasePriceSymbol(self, typeExchange, file=False):
        if not file:
            file = self.getRealPriceAllSymbol(typeExchange)
        with open(f"baseValues{typeExchange}.json", "w") as outfile:
            json.dump(file, outfile)
            print(f"Json file saved{typeExchange}")
            print(f"Base value update{typeExchange}")
