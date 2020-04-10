from db import mycursor, connection
import telebot
from telebot import types
from telebot.types import InputMediaPhoto, InputMediaVideo
import datetime
from datetime import datetime, timedelta
import re
import json

import faulthandler; faulthandler.enable()

TOKEN = '1009237691:AAGbCBSJAYBjVMruuTSCFAmNKRKYScvJ6aA'
date_pattern = re.compile(r'(\d{2}/\d{2})(?:\s+)?$')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_start(m):
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        after_tomorrow = datetime.now() + timedelta(days=2)
        tomorrow_formatted = tomorrow.strftime('%d/%m')
        after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')
        bot.send_message(m.chat.id, 'Привіт!\nЯ бот для домашнього завдання')
        bot.send_message(m.chat.id, f"Тобі потрібно добавити мене в групу або в чат.\nЩоб давити домашнє завдання, тобі потрібно добавити в кінці речення дату на яку потрібно виконати ДЗ, наприклад '{tomorrow_formatted}', '{after_tomorrow_formatted}' ")
        bot.send_photo(chat_id= m.chat.id, photo=open('img/Screenshot_3.png', 'rb'))
        bot.send_message(m.chat.id, f"А щоб дізнатися домашнє завдання, потрібно написати 'дз {tomorrow_formatted}', або 'ДЗ {after_tomorrow_formatted}'.\n Ти можеш детальні розібратися в /help ")
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')

@bot.message_handler(commands=['help'])
def keyboard_help(m):  # return keyboard
    try:
        help_list = 'ДЗ - дізнатися ДЗ на завтра, або на інший день\n\n/help_write_HW - Як записати домашнє завдання\n\n/help_return_HW - Як дізнатися домашнє завдання'
        bot.send_message(m.chat.id, help_list)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # keyboard
        markup.add('ДЗ',  )
        markup.add( '/help_write_HW')
        markup.add( '/return_HW')
        bot.send_message(m.chat.id, 'Зроби вибір',
                        reply_markup=markup)  # return keyboard
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')
    


@bot.message_handler(func=lambda m: m.text in ['ДЗ', 'Дз', 'дз'], content_types=['text'])
def tomorrow_HW(m):
    
    try:
        tomorrow = datetime.now()
        today_formatted = tomorrow.strftime('%d/%m')

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_formatted = tomorrow.strftime('%d/%m')
        
        after_tomorrow = datetime.now() + timedelta(days=2)
        after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')


        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('ДЗ' + today_formatted)
        markup.add('ДЗ ' + tomorrow_formatted)
        markup.add('ДЗ ' + after_tomorrow_formatted)
        bot.send_message(m.chat.id, 'Зроби вибір',
                        reply_markup=markup)
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')

@bot.message_handler(commands=['help_write_HW'])
def help_write_HW(m):
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_formatted = tomorrow.strftime('%d/%m')
        
        after_tomorrow = datetime.now() + timedelta(days=2)
        after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')

        bot.send_message(m.chat.id, f"Тобі потрібно добавити мене в групу або в чат.\nЩоб добавити домашнє завдання, тобі потрібно добавити в кінці речення дату на яку потрібно виконати ДЗ, наприклад '{tomorrow_formatted}', '{after_tomorrow_formatted}' ")
        bot.send_photo(chat_id= m.chat.id, photo=open('img/Screenshot_3.png', 'rb'))
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')

@bot.message_handler(commands=['return_HW'])
def return_HW(m):
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_formatted = tomorrow.strftime('%d/%m')
        
        after_tomorrow = datetime.now() + timedelta(days=2)
        after_tomorrow_formatted = after_tomorrow.strftime('%d/%m')

        bot.send_message(m.chat.id, f"Щоб дізнатися домашнє завдання, потрібно написати 'дз {tomorrow_formatted}', або 'ДЗ {after_tomorrow_formatted}'.")
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')


@bot.message_handler(func=lambda m: m.media_group_id != None, content_types=["photo"])
def photo_handler(m):
    print('<INCOMING PHOTO:\n')

    if m.media_group_id:
        save_photo(m)

        print(m.media_group_id, m.photo[-1].file_id)

        if m.caption:
            match = date_pattern.search(m.caption)

            if match:
                add_homework_gallery(m, match[1])
            else:
                bot.send_message(m.chat.id, 'Вкажіть дату ДЗ (add gallery)')
            
    else:
        match = date_pattern.search(m.caption)

        if match:
            add_homework(m, match[1])
        else:
            bot.send_message(m.chat.id, 'Вкажіть дату ДЗ (add photo)')

    print('\nEND PHOTO MESSAGE>\n\n')


@bot.message_handler(content_types=["text"])
def text_handler(m):
    # try:
    print('<INCOMING MESSAGE:\n')

    text = m.text #text = m.text if m.text else m.caption
    match = re.search(r'^(?:\s+)?(дз)?(?:.*)(\d{2}/\d{2})(?:\s+)?$', text, re.I)
    
    if match:
        date = match[2]
        if match[1]:
            print('Handle printing homework\n')
            print_homework(m, date)
        else:
            print('Handle adding homework\n')
            add_homework(m, date)
    else:
        print('Invalid message format\n')
        bot.send_message(m.chat.id, 'Вкажіть дату ДЗ')

    print('\nEND MESSAGE>\n\n')
    # except:
    #     bot.send_message(m.chat.id, 'Ой, щось поломалося, "text_handler" ')

def save_photo(m):
    print('save_photo')

    sql = "INSERT INTO media (media_group_id, msg_chat_id, file_id) VALUES (%s, %s, %s)"
    val = (m.media_group_id, m.chat.id, m.photo[-1].file_id)
    mycursor.execute(sql, val)
    connection.commit()

def add_homework_gallery(m, date):
    print('add_homework_gallery')
# try:
    media = json.dumps([m.media_group_id, m.caption])
    sql = "INSERT INTO message (msg_id, msg_chat_id, media, date) VALUES (%s, %s, %s, %s)"
    val = (m.message_id, m.chat.id, media, date)
    mycursor.execute(sql, val)
    connection.commit()
# except:
    # bot.send_message(m.chat.id, 'Ой, щось поломалося')


def add_homework(m, date):
    print('add_homework')

    try:
        sql = "INSERT INTO message (msg_id, msg_chat_id, date) VALUES (%s, %s, %s)"
        val = (m.message_id, m.chat.id, date)
        mycursor.execute(sql, val)
        connection.commit()
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')


    
def print_homework(m, date):
    print('print_homework')
    try:
        mycursor.execute(f"SELECT msg_id, msg_chat_id, media FROM message WHERE date = '{date}'")
        myresult = mycursor.fetchall()

        if len(myresult) == 0:
            bot.send_message(m.chat.id, 'Немає ДЗ на вказану дату')
            return
        
        for msg_id, msg_chat_id, media in myresult:
            if media != None:
                media_id, caption = json.loads(media)
                print('Prind HW data:', msg_id, msg_chat_id, media)
                print_gallery(m.chat.id, media_id, caption)
            else:
                bot.forward_message(m.chat.id, msg_chat_id, msg_id)

        
        print('\n----END PRINT HOMEWORK----\n\n')
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося (print_homework)')
        
                

def print_gallery(chat_id, media_id, caption):
    print('print_gallery')

    mycursor.execute(f"SELECT file_id FROM media WHERE media_group_id = '{media_id}'")
    myresult = mycursor.fetchall()
    photo_list = []
    
    for i in range(len(myresult)):
        photo = InputMediaPhoto(myresult[i][0])

        if i == 0:
            photo.caption = caption
        photo_list.append(photo)
    
    bot.send_media_group(chat_id, photo_list)


def select_date(m):
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # keyboard
        markup.add('ДЗ на завтра')  # add button
        bot.send_message(m.chat.id, 'Зробіть вибір',
                        reply_markup=markup)  # return keyboard
    except:
        bot.send_message(m.chat.id, 'Ой, щось поломалося')

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
connection.close()