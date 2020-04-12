from config import GET_ME
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def private_chat_kb():
    bot_link = "https://t.me/{}".format(GET_ME.username)
    button0 = InlineKeyboardButton(text="Private chat", url=bot_link)
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard