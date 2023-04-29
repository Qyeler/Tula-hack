from typing import List

from data.data_base import db_session
from data.data_base.items import Item
from data.data_base.users import User

db_session.global_init("./data/data_base.db")
session = db_session.create_session()


def update(current_cost: List[float]):
    session = db_session.create_session()
    for item, i in enumerate(session.query(Item).all()):
        item.minimal = min(current_cost[i], item.minimal)
    session.commit()

    for user in session.query(User):
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


def profile(user_id: int):
    session = db_session.create_session()

    user = session.query(User).filter(User.telegram_id == user_id).first()
    user_list = user.items.split("|")
    message = ""
    for item_id in user_list:
        if item_id == "": continue
        item_id = int(item_id)
        item = session.query(Item).filter(Item.id == item_id).first()
        message += item.name + "\n" +item.minimal + "\n" + item.link + "\n"

    ####### send message #############
    # if message:
    #     send_message(user.telegram_id, "Список ваших товаров:\n" + message)
    ####################################

    session.close()

def add_item(name, cost, link):
    session = db_session.create_session()
    item = Item()
    item.name = name
    item.minimal = cost
    item.link = link
    session.commit()
    session.add(item)
    session.close()


def add_user(telegram_id):
    session = db_session.create_session()
    user = User()
    user.telegram_id = telegram_id

    session.add(user)
    session.commit()

    session.close()



