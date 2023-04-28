import telebot
from telebot import types
bot = telebot.TeleBot("6163085124:AAFcH7JLOfSmFTi8WmdhwdodlssgeVi3Z_Q")

# @bot.message_handler(commands=['start'])
# def start_handler(message):
#     bot.send_message(message.chat.id, "Привет, я бот команды <Тульский пряник>, рад тебя видеть! "
#                                       "Я могу помочь тебе отслеживать цены на товары. Введи название товара или ссылку на него, чтобы начать."
#                                       "Мы пока что поддерживаем товары только c этих сайтов\n"
#                                       "Wildberries\n"
#                                       "Ozon\n"
#                                       "Aliexpress\n"
#                                       "Yandex_market\n"
#                                       "Более подробно можно узнать командой /help")
@bot.message_handler(commands=['start'])
def start_handler(message):
    # создаем клавиатуру с inline-кнопками
    markup = types.InlineKeyboardMarkup()
    btn_wildberries = types.InlineKeyboardButton('Wildberries', url='https://www.wildberries.ru/')
    btn_ozon = types.InlineKeyboardButton('Ozon', url='https://www.ozon.ru/')
    btn_yandex_market = types.InlineKeyboardButton('Yandex Market', url='https://market.yandex.ru/')
    btn_aliexpress = types.InlineKeyboardButton('Aliexpress', url='https://aliexpress.ru/')
    markup.row(btn_wildberries, btn_ozon)
    markup.row(btn_yandex_market, btn_aliexpress)

    bot.send_message(message.chat.id, "Привет, я бот команды {Тульский пряник}, рад тебя видеть! "
                                      "\nВ мой функционал входит:\n"
                                      "\n1) Показывать наиболее выгодные предложения покупки товара\n"
                                      "\n2) Начать мониторинг цены на нужный вам товар\n"
                                      "\n3) Попробывать предсказать ценник товара\n"
                                      "\nВведите /help чтобы более подробно узнать о функционале"
                                      "\nВведи название товара или ссылку на него, чтобы начать.\n"
                                      "Мы пока что поддерживаем товары только c этих сайтов\n",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    text = message.text.lower()
    if text.startswith("https://www.wildberries.ru/catalog/"):
        process_wildberries_link(message)
    elif text.startswith("https://www.ozon.ru/product/"):
        process_ozon_link(message)
    elif text.startswith("https://market.yandex.ru/product-"):
        process_yandex_link(message)
    elif text.startswith("https://aliexpress.ru/item/"):
        process_aliexpress_link(message)
    else:
        process_title(message)

def process_wildberries_link(message):
    bot.send_message(message.chat.id, "Это Вайлберис товар")
def process_ozon_link(message):
    bot.send_message(message.chat.id,"Это Озон товар")
def process_yandex_link(message):
    bot.send_message(message.chat.id,"Это Яндекс товар")
def process_aliexpress_link(message):
    bot.send_message(message.chat.id,"Это Алиэкспресс")
def process_title(message):
    if(message.text=="/help"):
        bot.send_message(message.chat.id,("Блин надо сделать хельп"))
    else:
        bot.send_message(message.chat.id,"Это название товара надопробить по всем базам")


if __name__ == '__main__':

    bot.polling(none_stop=True)