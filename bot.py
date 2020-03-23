from db import mycursor, mydb
import telebot
from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo
import re
import datetime
from datetime import datetime, timedelta
import json

TOKEN = '1009237691:AAGbCBSJAYBjVMruuTSCFAmNKRKYScvJ6aA'
date_pattern = re.compile(r'(\d{2}/\d{2})(?:\s+)?$')
bot = telebot.TeleBot(TOKEN)
media = {
    'g_id': None,
    'media_list': [],
    'caption': ''
}

@bot.message_handler(commands=['start'])
def command_start(m):
    tomorrow = datetime.now() + timedelta(days=1)
    after_tomorrow = datetime.now() + timedelta(days=2)
    tomorrow_formatted = tomorrow.strftime('%d/%m')
    after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')
    bot.send_message(m.chat.id, 'Привіт!\nЯ бот для домашнього завдання')
    bot.send_message(m.chat.id, f"Тобі потрібно добавити мене в групу або в чат.\nЩоб давити домашнє завдання, тобі потрібно добавити в кінці речення дату на яку потрібно виконати ДЗ, наприклад '{tomorrow_formatted}', '{after_tomorrow_formatted}' ")
    bot.send_photo(chat_id= m.chat.id, photo=open('img/Screenshot_3.png', 'rb'))
    bot.send_message(m.chat.id, f"А щоб дізнатися домашнє завдання, потрібно написати 'дз {tomorrow_formatted}', або 'ДЗ {after_tomorrow_formatted}'.\n ти можеш детальні розібратися в /help ")


@bot.message_handler(commands=['help'])
def keyboard_help(m):  # return keyboard
    help_list = 'ДЗ - дізнатися ДЗ на завтра, або на інший день\n\n/help_write_HW - Як записати домашнє завдання\n\n/help_return_HW - Як дізнатися домашнє завдання'
    bot.send_message(m.chat.id, help_list)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # keyboard
    markup.add('ДЗ',  )
    markup.add( '/help_write_HW')
    markup.add( '/return_HW')
    bot.send_message(m.chat.id, 'Зроби вибір',
                     reply_markup=markup)  # return keyboard


@bot.message_handler(func=lambda m: 'ДЗ' == m.text, content_types=['text'])
def tomorrow_HW(m):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%d/%m')
    
    after_tomorrow = datetime.now() + timedelta(days=2)
    after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')

    after_after_tomorrow = datetime.now() + timedelta(days=3)
    after_after_tomorrow_formatted = after_after_tomorrow.strftime('%d/%m')

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('ДЗ ' + tomorrow_formatted)
    markup.add('ДЗ ' + after_tomorrow_formatted)
    markup.add('ДЗ ' + after_after_tomorrow_formatted)
    bot.send_message(m.chat.id, 'Зроби вибір',
                     reply_markup=markup)

@bot.message_handler(commands=['help_write_HW'])
def help_write_HW(m):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%d/%m')
    
    after_tomorrow = datetime.now() + timedelta(days=2)
    after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')

    bot.send_message(m.chat.id, f"Тобі потрібно добавити мене в групу або в чат.\nЩоб добавити домашнє завдання, тобі потрібно добавити в кінці речення дату на яку потрібно виконати ДЗ, наприклад '{tomorrow_formatted}', '{after_tomorrow_formatted}' ")
    bot.send_photo(chat_id= m.chat.id, photo=open('img/Screenshot_3.png', 'rb'))

@bot.message_handler(commands=['return_HW'])
def return_HW(m):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_formatted = tomorrow.strftime('%d/%m')
    
    after_tomorrow = datetime.now() + timedelta(days=2)
    after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')

    bot.send_message(m.chat.id, f"Щоб дізнатися домашнє завдання, потрібно написати 'дз {tomorrow_formatted}', або 'ДЗ {after_tomorrow_formatted}'.")




@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def m_handler(m):
    print('INCOMING MESSAGE:\n')
    
    g_id = m.media_group_id
    
    if g_id:
        f_id = m.photo[-1].file_id
        
        if media['g_id'] == g_id:
            if f_id not in media['media_list']:
                media['media_list'].append(f_id) 
                if m.caption:
                    media['caption'] = m.caption
        else:
            print('media_id (g_id): ', media['g_id'])
            
            if media['g_id'] != None:
                save_gallery(m)
                print('cleared', media)
                
            media['g_id'] = g_id
            media['media_list'] = [f_id]             
            if m.caption:
                media['caption'] = m.caption
    else:
        print('Обробляємо не галерею \n ')
        if media['g_id']:
            save_gallery(m)
        
        text = m.text if m.text else m.caption
        match = re.search(r'^(?:\s+)?(дз)?(?:.*)(\d{2}/\d{2})(?:\s+)?$', text, re.I)
        
        if match:
            date = match[2]
            if match[1]:
                print('Обробляємо виведення дз \n ')
                print_homework(m, date)
            else:
                print('Обробляємо додавання дз \n ')
                add_homework(m, date)
        else:
            bot.send_message(m.chat.id, 'Введіть дату ДЗ')

    print(media, m.caption, '\n\nEND MESSAGE\n\n')


def save_gallery(m):
    print('save_gallery\n')
    global media
    match = date_pattern.search(media['caption'])
    chat_id, msg_id = m.chat.id, m.message_id

    if match:
        gallery = json.dumps(media)
        date = match[0]
        print('save_gallery', media)
        sql = "INSERT INTO message (msg_id, msg_chat_id, media, date) VALUES (%s, %s, %s, %s)"
        val = (msg_id, chat_id, gallery, date)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        bot.send_message(chat_id, f'введіть дату (save gallery)\ncaption: {media["caption"]}')
        print('save gallery match: ', match)
    
    media = {
        'g_id': None,
        'media_list': [],
        'caption': ''
    }


def add_homework(m, date):
    chat_id, msg_id = m.chat.id, m.message_id
    sql = "INSERT INTO message (msg_id, msg_chat_id, date) VALUES (%s, %s, %s)"
    val = (msg_id, chat_id, date)
    mycursor.execute(sql, val)
    mydb.commit()


    
def print_homework(m, date):
    mycursor.execute(f"SELECT msg_id, msg_chat_id, media FROM message WHERE date ='{date}'")
    myresult = mycursor.fetchall()
    
    for msg_id, msg_chat_id, media in myresult:
        if media != None:
            print('Prind HW data:', msg_id, msg_chat_id, media)
            print_gallery(m.chat.id, media)
        else:
            bot.forward_message(m.chat.id, msg_chat_id, msg_id)
    
                

def print_gallery(chat_id, media_json):
    md = json.loads(media_json)
    photo_list = []
    for i in range(len(md['media_list'])):
        photo = InputMediaPhoto(md['media_list'][i])
        if i==0:
            photo.caption = md['caption']
        photo_list.append(photo)
    # print(md)
    bot.send_media_group(chat_id, photo_list)


def select_date(m):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # keyboard
    markup.add('ДЗ на завтра')  # add button
    bot.send_message(m.chat.id, 'Зробіть вибір',
                     reply_markup=markup)  # return keyboard

# @bot.message_handler(func=lambda m: "ДЗ на завтра" == m.text, content_types=['text'])
# def tomorrow_HW(m):
#    tomorrow = datetime.now() + timedelta(days=1)
#    tomorrow_formatted = tomorrow.strftime('%d/%m')
#    sql = f"SELECT msg_chat_id, msg_id FROM message WHERE date ='{tomorrow_formatted}'"
#    mycursor.execute(sql)
#    myresult = mycursor.fetchall()
#    for (msg_chat_id, msg_id) in myresult:
#       bot.forward_message(chat_id, msg_chat_id, msg_id)



bot.polling()
 