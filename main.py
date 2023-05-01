import random

import telebot
import seleniumReal
from telebot import types
import functions
from parsSite import ctlpars, ozonpars, pritserupars, parswld
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

bot = telebot.TeleBot("")
admin_key=""
@bot.message_handler(commands=['profile'])
def profile_handler(message):
    bot.send_message(message.chat.id, "Ваш профиль:\n"+functions.profile(message.chat.id)+"\n",disable_web_page_preview=True,parse_mode="HTML")

@bot.message_handler(commands=['update'])
def profile_handler(message):
    print(str(message.chat.id))
    if(str(message.chat.id)==admin_key):
        text=message.text.split()[1]
        if(text=="fake"):
            messages = functions.update(fake_update())
        else:
            messages=functions.update(min_for_updates())
        for j in messages:
            bot.send_message(j[1],j[0])
    else:
        bot.send_message(message.chat.id, "У вас нет прав")
@bot.message_handler(commands=['delete'])
def profile_handler(message):
    name_item=message.text.split(" ")[1]
    if str(name_item).isdigit():
        functions.delete_item(message.chat.id,name_item)
        bot.send_message(message.chat.id, "Успешно")
    else:
        bot.send_message(message.chat.id, "Второй параметр не является числом")
@bot.message_handler(commands=['start'])
def start_handler(message):
    # создаем клавиатуру с inline-кнопками
    markup = types.InlineKeyboardMarkup()
    btn_wildberries = types.InlineKeyboardButton('Citilink', url='https://www.citilink.ru/')
    btn_ozon = types.InlineKeyboardButton('Ozon', url='https://www.ozon.ru/')
    btn_yandex_market = types.InlineKeyboardButton('Price ru', url='https://price.ru/')
    markup.row(btn_wildberries, btn_ozon)
    markup.row(btn_yandex_market)

    bot.send_message(message.chat.id, "Привет, я бот команды {Тульский пряник}, рад тебя видеть! "
                                      "\nВ мой функционал входит:\n"
                                      "\n1) Показывать наиболее выгодные предложения покупки товара\n"
                                      "\n2) Начать мониторинг цены на нужный вам товар\n"
                                      "\n3) Попробывать предсказать ценник товара\n"
                                      "\nВведите /help чтобы более подробно узнать о функционале"
                                      "\nВведи название товара или ссылку на него, чтобы начать.\n"
                                      "Мы пока что поддерживаем товары только c этих сайтов\n",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.reply_to_message is not None or message.forward_from is not None or message.forward_from_chat is not None)
def reply_handler(message):
    functions.add_user(message.chat.id)
    try:
        text=str(message.text)
        name=text[9:text.find("Стоимость:")-1]
        cost=text[text.find('Стоимость:')+10:-1]
        link=message.json['reply_markup']['inline_keyboard'][0][0]['url']
        functions.add_item(name, cost, link, message.chat.id)
    except:
        bot.send_message(message.chat.id,"Вы переслали товар, который я не могу отслеживать =(\n")
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    print(message.reply_to_message)
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
                                          "\n 2) Перешлите сообщение с товаром, который вас заинтересовал, чтобы добавить его отслеживание в личный кабинет\n"
                                          "\n 3) Отправьте команду /profile, чтобы получить информацию о товарах, которые вы пересылали\n"
                                          "\n 4) Отправьте команду /delete номер в списке в профиле, чтобы удалить товар из отслеживающихся\n"
                                          "\nПод базой данных мы имеем ввиду сайты: citilink, ozon, price_ru\n"
                                          "Этот список будет пополняться\n"
                                          "\n Разработкой бота занималась команда Тульский пряник\n Контактный email: nikitanaz12@gmail.com"))
    else:
        if (message.text[0]=='/'):
            bot.send_message(message.chat.id, ("Такой команды не существует"))
            return
        if (len(message.text) <= 5):
            bot.send_message(message.chat.id, ("Вы ввели данные, по которым мы не можем реализовать поиск=("))
            return
        bot.send_message(message.chat.id,"Ищу название товара в базах ожидание может занять от 1-4 минут...\n"
                                         "Если хотите отслеживать товар перешлите нам сообщение с интересующим вас предложением\n")
        ansDict=findAns(message.text)
        if(len(ansDict)==0):
            bot.send_message(message.chat.id,"Извините, я не смог ничего найти по вашему запросу...")
        for i in ansDict:
            markup = types.InlineKeyboardMarkup()
            btn_tmp = types.InlineKeyboardButton('Ссылка на товар', url=i["link"])
            markup.row(btn_tmp)
            bot.send_message(message.chat.id, "Название: "+str(i["name"][0]).upper()+i["name"][1:]+"\n"+ "Стоимость: "+ i["price"]+"₽\n",disable_web_page_preview=True,reply_markup=markup)#
        bot.send_message(message.chat.id,"Если хотите отслеживать товар перешлите нам сообщение с интересующим вас предложением\n")

def findAns(name):
    name=str(name).lower()
    arr={"answer":[]}
    sites=["https://www.ozon.ru/search/?text=","https://www.citilink.ru/search/?text=","https://price.ru/search/?query=","https://www.wildberries.ru/catalog/0/search.aspx?search="]
    for i in sites:
        match(i[0:23]):
            case("https://www.citilink.ru"):
                HTML = seleniumReal.getHTML(i + name)
                for k in ctlpars(HTML):
                    if k['name'].find(name.split()[0]):
                        arr["answer"].append(k)
            case("https://www.ozon.ru/sea"):
                HTML = seleniumReal.getHTML(i + name)
                for k in ozonpars(HTML):
                    if k['name'].find(name.split()[0]):
                        arr["answer"].append(k)
            case("https://price.ru/search"):
                for k in pritserupars(i + name):
                    if k['name'].find(name.split()[0]):
                        arr["answer"].append(k)
            case("https://www.wildberries"):
                HTML = seleniumReal.getHTML(i + name)
                for k in parswld(HTML):
                    print(k)
                    if k['name'].find(name.split()[0]):
                        arr["answer"].append(k)
    #[{"price":"","link":"","name":""}]
    arr["answer"].sort(key=lambda x:int(x['price']))
    answer = arr["answer"][:10]
    return(answer)

def fake_update():
    arr = functions.item_titles()
    fake_arr=[]
    for i in range(len(arr)):
        fake_arr.append(5)
    return(fake_arr)
def min_for_updates():
    arr= functions.item_titles()
    updates=[]
    for i in arr:
        updates.append(findAns(str(i)[0]['price']))
    return(updates)

if __name__ == '__main__':
    bot.polling(none_stop=True)
