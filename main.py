import telebot
import seleniumReal
from telebot import types

from parsSite import ctlpars

bot = telebot.TeleBot("6163085124:AAFcH7JLOfSmFTi8WmdhwdodlssgeVi3Z_Q")

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
        process_link(message,"wld")
    elif text.startswith("https://www.ozon.ru/product/"):
        process_link(message,"ozn")
    elif text.startswith("https://market.yandex.ru/product-"):
        process_link(message,"ydx")
    elif text.startswith("https://aliexpress.ru/item/"):
        process_link(message,"ali")
    else:
        process_title(message)

def process_link(message,name_company):
    bot.send_message(message.chat.id, "Это ссылка на товар")
    match name_company:
        case "wld":
            print("Это товар с wildb")
        case "ozn":
            print("Это товар с ozon")
        case "ydx":
            print("Это товар с yandexMrk")
        case "ali":
            print("Это товар с aliex")
        case "stl":
            print("Это товар с sitilink")

def process_title(message):
    if(message.text=="/help"):
        bot.send_message(message.chat.id,("Блин надо сделать хельп"))
    else:
        bot.send_message(message.chat.id,"Ищу название товара в базах...")
        HTML=seleniumReal.getHTML("https://www.citilink.ru/search/?text="+message.text)
        ansDict=ctlpars(HTML)
        for i in ansDict['answer']:
            bot.send_message(message.chat.id, "Название: "+i["name"][0:36]+"\n"+ "Стоимость: "+ i["price"]+"\n"+"Ссылка на товар:\n"+i["link"]+"\n")

if __name__ == '__main__':
    bot.polling(none_stop=True)