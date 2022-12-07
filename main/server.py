import time
import config
import symbols
import telebot
import threading


class Server():

    token = open('TgToken.txt', 'r').read()
    bot = telebot.TeleBot(token)
    stop = False

    def server(self, tgId):

        CONFIG = config.Config()
        __frequencyRefrashBaseValue = CONFIG.getConfig()[
            "frequencyRefrashBaseValue"]
        __minChangeABS = CONFIG.getConfig()["minChangeABS"]
        __frequencyRefrashRealValue = CONFIG.getConfig()[
            "frequencyRefrashRealValue"]
        symbols.Symbols().setBasePriceSymbol("futures")
        symbols.Symbols().setBasePriceSymbol("spot")
        i = 0

        while True:

            if self.stop:
                return

            sumbols = symbols.Symbols()
            priceBaseFutures = sumbols.getBasePriceAllSymbol("futures")
            priceRealFutures = sumbols.getRealPriceAllSymbol("futures")
            priceBaseSpot = sumbols.getBasePriceAllSymbol("spot")
            priceRealSpot = sumbols.getRealPriceAllSymbol("spot")

            if priceBaseFutures[0]['symbol'] != priceRealFutures[0]['symbol']:
                time.sleep(1)
                continue

            else:
                thread1 = threading.Thread(
                    target=self.__comparison,
                    name="checkComp1",
                    daemon=None,
                    args=[
                        priceRealFutures,
                        priceBaseFutures,
                        tgId,
                        "futures",
                        __minChangeABS])

                thread2 = threading.Thread(
                    target=self.__comparison,
                    name="checkComp2",
                    daemon=None, args=[
                        priceRealSpot,
                        priceBaseSpot,
                        tgId,
                        "spot",
                        __minChangeABS])

                thread1.start()
                thread2.start()
                differenceTime = 60 * \
                    int(__frequencyRefrashBaseValue) / 60 * float(__frequencyRefrashRealValue)

                if (differenceTime <= 1):
                    differenceTime = 1

                if i >= differenceTime:
                    i = 0
                    print("Resave base value!")
                    sumbols.setBasePriceSymbol("futures")
                    sumbols.setBasePriceSymbol("spot")

                else:
                    i += 1

            time.sleep(60 * float(__frequencyRefrashRealValue))

    def __comparison(
            self,
            realValues,
            baseValues,
            tgId,
            typeExchange,
            __minChangeABS):

        if typeExchange == "futures":
            priceName = "lastPrice"
        else:
            priceName = "price"

        for i in range(len(baseValues)):
            difference = (
                (float(
                    realValues[i][priceName]) -
                    float(
                    baseValues[i][priceName])) /
                float(
                    realValues[i][priceName]) *
                100)
            if abs(difference) >= float(__minChangeABS):
                print(f"Цена {baseValues[i]['symbol'] + ' ' + typeExchange} упала на {round(abs(difference), 4)}% \nПервоначальная цена:{baseValues[i][priceName]} \nЦена на текущий момент :{realValues[i][priceName]}")
                if str(difference)[0] == "-":
                    print()
                    self.bot.send_message(
                        tgId,
                        f"Цена {baseValues[i]['symbol'] + ' ' + typeExchange} упала на {round(abs(difference), 4)}% \nПервоначальная цена:{baseValues[i][priceName]} \nЦена на текущий момент :{realValues[i][priceName]}")
                else:
                    self.bot.send_message(
                        tgId,
                        f"Цена {baseValues[i]['symbol'] + ' ' + typeExchange} выросла на {round(abs(difference), 4)}% \nПервоначальная цена:{baseValues[i][priceName]} \nЦена на текущий момент :{realValues[i][priceName]}")

                baseValues[i][priceName] = realValues[i][priceName]
                symbols.Symbols().setBasePriceSymbol(typeExchange, baseValues)
