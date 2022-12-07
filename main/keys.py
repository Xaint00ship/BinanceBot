from telebot import types


class Buttons():

    mainBtn = [
        types.KeyboardButton("Настройки"),
        types.KeyboardButton("Запуск"),
        types.KeyboardButton("Стоп")
    ]
    settingBtn = [
        types.KeyboardButton("Базовые значения"),
        types.KeyboardButton("Отклонения"),
        types.KeyboardButton("Актуальные данные"),
        types.KeyboardButton("Назад")
    ]

    def addMainBtn(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in self.mainBtn:
            markup.add(self.mainBtn[i])
        return markup

    def addSettingBtn(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in self.settingBtn:
            markup.add(self.settingBtn[i])
        return markup
