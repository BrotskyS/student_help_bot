import re
import json
from debug_data import ml
from db import mycursor, mydb
import datetime
from datetime import datetime, timedelta

media = {
    'g_id': None,
    'media_list': [],
    'caption': ''
}

def error(text):
    print(f'\n\nERROR:\n{text}\n\n')

def InputMediaPhoto(file_id):
    for m in ml:
        if m.photo and m.photo[-1].file_id == file_id:
            return m

def forward_message(to_id, from_id, msg_id):
    for m in ml:
        if m.message_id == msg_id:
            send_message(to_id, m.text)
            return
    else:
        error('MSG id to forward isn\'t exist')

def send_message(chat_id, msg):
    print(f'\n-----SEND MESSAGE-----\n\nchat_id: {chat_id}\nmessage text: {msg}\n\n')

def send_media_group(chat_id, media_list):
    print(f'\n-----SEND MEDIA GROUP-----\n\nchat_id: {chat_id}\n')
    for media in media_list:
        print(media)
    print(f'----END MEDIA GROUP----\n\n')


TOKEN = '1009237691:AAGbCBSJAYBjVMruuTSCFAmNKRKYScvJ6aA'
date_pattern = re.compile(r'(\d{2}/\d{2})(?:\s+)?$')
#bot = telebot.TeleBot(TOKEN)
media = {
    'g_id': None,
    'media_list': [],
    'caption': ''
}

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
            print('old media_id (g_id): ', media['g_id'])
            
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
            send_message(m.chat.id, 'Введіть дату ДЗ')

    print(media, m.caption, '\n\nEND MESSAGE\n\n')


def save_gallery(m):
    print('save_gallery\n')
    global media
    match = date_pattern.search(media['caption'])
    chat_id, msg_id = m.chat.id, m.message_id

    if match:
        gallery = json.dumps(media)
        date = match[0]
        print('adding to DB', media)
        sql = "INSERT INTO message (msg_id, msg_chat_id, media, date) VALUES (%s, %s, %s, %s)"
        val = (msg_id, chat_id, gallery, date)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        send_message(chat_id, f'введіть дату (save gallery)\ncaption: {media["caption"]}')
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
            forward_message(m.chat.id, msg_chat_id, msg_id)
    
                

def print_gallery(chat_id, media_json):
    fetched_media = json.loads(media_json)
    photo_list = []
    for i in range(len(fetched_media['media_list'])):
        photo = InputMediaPhoto(fetched_media['media_list'][i])
        if i == 0:
            photo.caption = fetched_media['caption']
        photo_list.append(photo)
    # print(fetched_media)
    send_media_group(chat_id, photo_list)


#bot.polling()
 

for m in ml:
    m_handler(m)

