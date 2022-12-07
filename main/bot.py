import telebot
import threading
import server
import config
import keys

token = open('TgToken.txt', 'r').read()
checkedStratServer = [0]
bot = telebot.TeleBot(token)
serv = server.Server()
btns = keys.Buttons()


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(
        m.chat.id,
        "Бот для отслеживания аномальных скачаков USD-M на бирже Binance",
        reply_markup=btns.addMainBtn())


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Настройки':
        bot.send_message(
            message.chat.id,
            "Настройки",
            reply_markup=btns.addSettingBtn())

    elif message.text.strip() == 'Запуск':
        if checkedStratServer[0] == 0:
            checkedStratServer[0] = 1
            serv.stop = False
            tg_id = message.chat.id
            thread = threading.Thread(
                target=serv.server,
                name="server",
                daemon=None,
                args=[tg_id])
            thread.start()
            print("Start server")
            bot.send_message(message.chat.id, f"Запуск отслеживания")
        else:
            bot.send_message(message.chat.id, f"Отслеживание уже запущено")

    elif message.text.strip() == 'Базовые значения':
        bot.send_message(
            message.chat.id,
            "Введите время обновления базовых значений(мин)")
        bot.register_next_step_handler(message, setFrequencyRefrashBaseValue)

    elif message.text.strip() == 'Отклонения':
        bot.send_message(
            message.chat.id,
            "Введите минимальные отклонение от базовой цены (%)")
        bot.register_next_step_handler(message, setMinChangeABS)

    elif message.text.strip() == 'Актуальные данные':
        bot.send_message(
            message.chat.id,
            "Введите время обновления актуальных данных (мин)")
        bot.register_next_step_handler(message, setFrequencyRefrashRealValue)

    elif message.text.strip() == 'Назад':
        bot.send_message(
            message.chat.id,
            "Главное меню",
            reply_markup=btns.addMainBtn())

    elif message.text.strip() == "Стоп":
        if checkedStratServer[0] == 1:
            checkedStratServer[0] = 0
            serv.stop = True
            print("Stop server")
            bot.send_message(message.chat.id, f"Остановка отслеживания")
        else:
            bot.send_message(message.chat.id, f"Отслеживание не запущено")


def setFrequencyRefrashBaseValue(message):
    try:
        if abs(int(message.text)) >= 0:

            configFile = config.Config().getConfig()
            configFile["frequencyRefrashBaseValue"] = message.text
            config.Config().setConfig(configFile)
            bot.send_message(
                message.chat.id,
                f"Данные обновлены, время обновления базовых значений({message.text} мин)")
    except BaseException:
        bot.send_message(message.chat.id, f"Некорректные данные")


def setMinChangeABS(message):
    try:
        int(message.text)
        configFile = config.Config().getConfig()
        configFile["minChangeABS"] = message.text
        config.Config().setConfig(configFile)

        bot.send_message(
            message.chat.id,
            f"Данные обновлены, отклонение от базовой цены ({message.text} %)")
    except BaseException:
        bot.send_message(message.chat.id, f"Некорректные данные")


def setFrequencyRefrashRealValue(message):
    try:
        float(message.text)
        configFile = config.Config().getConfig()
        configFile["frequencyRefrashRealValue"] = message.text
        config.Config().setConfig(configFile)

        bot.send_message(
            message.chat.id,
            f"Данные обновлены, время обновления актуальных данных ({message.text} мин)")
    except BaseException:
        bot.send_message(message.chat.id, f"Некорректные данные")


bot.infinity_polling()
