from typing import List

from data.data_base import db_session
from data.data_base.items import Item
from data.data_base.users import User

db_session.global_init("./data/data_base.db")
session = db_session.create_session()


def update(current_cost):
    session = db_session.create_session()
    for item, i in enumerate(session.query(Item).all()):
        item.minimal = min(current_cost[i], item.minimal)
    session.commit()

    for user in session.query(User).all():
        message = ""
        costs = list(map(float, user.items_cost.split("|")))
        for i in user.items.split('|'):
            if i == '': continue
            it = int(i)
            item = session.query(Item).filter(Item.id == it).first()
            if item.minimal < 0.95 * costs[it]:
                message += f"Акция! Товар {item.name} подешевел\n"

        # send telegram message #######################
        # if message:                                 #
        #     send_message(user.telegram_id, message) #
        ###############################################
    session.close()
    return message



def profile(user_id):
    session = db_session.create_session()

    user = session.query(User).filter(User.telegram_id == user_id).first()
    user_list = user.items.split("|")
    message = ""
    count=1
    for item_id in user_list:
        if item_id == "": continue
        item_id = int(item_id)
        item = session.query(Item).filter(Item.id == item_id).first()
        message +=str(count)+") Название: " + item.name + "\n Стоимость товара: " +item.minimal + "\n Ссылка на товар: " + f"Нажми <a href='{item.link}'>здесь</a>"+ "\n\n"
        count+=1
    ####### send message #############
    # if message:
    #     send_message(user.telegram_id, "Список ваших товаров:\n" + message)
    ####################################
    session.close()
    return (message)

def delete_item(user_id, num):
    num=int(num)
    num -= 1

    session = db_session.create_session()
    user = session.query(User).filter(User.telegram_id == user_id).first()
    if len(user.items_cost.split('|')) < num:
        return
    user.items_cost = '|'.join(user.items_cost.split('|')[:num] + user.items_cost.split('|')[num + 1:])
    user.items = '|'.join(user.items.split('|')[:num] + user.items.split('|')[num + 1:])

    session.commit()
    session.close()


def add_item(name, cost, link, user_id):
    name, cost, link, user_id = map(str, [name, cost, link, user_id])
    session = db_session.create_session()
    item = session.query(Item).filter(Item.name == name).first()
    if not item:
        item = Item()
        item.name = name
        item.minimal = cost
        item.link = link
        session.add(item)
        session.commit()
    user = session.query(User).filter(User.telegram_id == user_id).first()
    if not user:
        add_user(user_id)
    item = session.query(Item).filter(Item.name == name).first()
    user = session.query(User).filter(User.telegram_id == user_id).first()
    user.items += ("|" if user.items != '' else "") + str(item.id)
    user.items_cost += ("|" if user.items_cost != '' else "") + cost

    session.commit()
    session.close()


def add_user(telegram_id):
    session = db_session.create_session()
    if session.query(User).filter(User.telegram_id == str(telegram_id)).first(): return
    user = User()
    user.telegram_id = telegram_id
    user.items = ""
    user.items_cost = ""

    session.add(user)

    session.commit()
    session.close()