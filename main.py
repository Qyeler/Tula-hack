import telebot
import seleniumReal
from telebot import types

from parsSite import ctlpars, ozonpars, pritserupars

bot = telebot.TeleBot("6163085124:AAFcH7JLOfSmFTi8WmdhwdodlssgeVi3Z_Q")

@bot.message_handler(commands=['start'])
def start_handler(message):
    # создаем клавиатуру с inline-кнопками
    markup = types.InlineKeyboardMarkup()
    btn_wildberries = types.InlineKeyboardButton('Citilink', url='https://www.citilink.ru/')
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
            print("Это товар с ctln")

def process_title(message):
    if(message.text=="/help"):
        bot.send_message(message.chat.id,("В данный момент реализованн функционал:\n"
                                          "\n 1) Напишите название товара, мы пробьем его по базам и покажем каике ценники мы смогли найти\n"
                                          "\nПод базой данных мы имеем ввиду сайты: citilink,\n"
                                          "Этот список будет пополняться\n"
                                          "\n Разработкой бота занималась команда Тульский пряник\n Контактный email: nikitanaz12@gmail.com"))
    else:
        bot.send_message(message.chat.id,"Ищу название товара в базах...")
        ansDict=findAns(message.text)
        for i in ansDict:
            bot.send_message(message.chat.id, "Название: "+i["name"][0:36]+"\n"+ "Стоимость: "+ i["price"]+"\n"+"Ссылка на товар:\n"+i["link"]+"\n",disable_web_page_preview=True)
        bot.send_message(message.chat.id,"Если хотите отслеживать товар перешлите нам сообщение с интересующим вас предложением\n")

def findAns(name):
    arr={"answer":[]}
    sites=["https://www.citilink.ru/search/?text=","https://price.ru/search/?query="]#,"https://www.ozon.ru/search/?text=",]
    for i in sites:
        HTML = seleniumReal.getHTML(i + name)
        match(i[0:23]):
            case("https://www.citilink.ru"):
                for k in ctlpars(HTML):
                    arr["answer"].append(k)
            case("https://www.ozon.ru/sea"):
                for k in ozonpars(HTML):
                    arr["answer"].append(k)
            case("https://price.ru/search"):
                for k in pritserupars(i + name):
                    arr["answer"].append(k)
    #[{"price":"","link":"","name":""}]
    arr["answer"].sort(key=lambda x:int(x['price']))
    answer = arr["answer"][:10]
    '''
    for i in arr["answer"]:
        if(len(answer)<10):
            answer.append(i)
        else:
            for _ in range(10):#Здесь можно исполльзовать че-нибудь сортированное, но сейчас 12 ночи...
                if(int(i["price"])<int(answer[_]["price"])):
                    answer[_] = i
    '''
    return(answer)

@bot.message_handler(func=lambda message: message.forward_from is not None)
def handle_forwarded_message(message):
    forwarded_message = message.forward_from
    original_text = forwarded_message.text
    print(original_text)

if __name__ == '__main__':
    bot.polling(none_stop=True)