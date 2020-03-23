import re
import json
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="root",
    port='3306',
	database='telebot'

)
mycursor = mydb.cursor()

class Message:
    chat = type('obj', (object,), {'id' : '123'})
    def __init__(self, m_id, g_id=None, photo=None, caption=''):
        self.media_group_id = g_id
        self.message_id = m_id
        self.caption = caption
        self.photo = [type('obj', (object,), {'file_id' : photo})] if photo else []
ml = [
    Message(55, 334456, 'Awsdfseasdzxc', '05/12'),
    Message(555, 334456, 'Bdfasdzxc'),
    Message(536, 4534456, 'Cweaasdqsdzxc', '05/12'),
    Message(456, 4534456, 'Dweasdzxc'),
]

media = {
    'g_id': None,
    'media_list': [],
    'caption': ''
}



def print_mess(chat_id,m):
    print('message: ', m)
def m_handler(m):
    global print_mess
    g_id = m.media_group_id
    if g_id:
        f_id = m.photo[-1].file_id
        if media['g_id'] == g_id:
            if f_id not in media['media_list']:
                media['media_list'].append(f_id)
                if m.caption:
                    media['caption'] = m.caption
        else:
            print('media_id: ', media['g_id'])
            if media['g_id'] != None:
                save_gallery(m)
                print('cleared', media)
                
            media['g_id'] = g_id
            media['media_list'] = [f_id]
            if m.caption:
                media['caption'] = m.caption
    else:
        print('hello')
        save_gallery(m)
        match = re.search(r'\d{2}/\d{2}$', m.text)
        if match:
            # add_homework(m, match[0])
            print_mess(m.chat.id, 'aaaaaaaaabot ')
        else:
            print_mess(m.chat.id, 'Введіть дату ')
    print(media, m.caption, '\n\n')


def save_gallery(m):
    global media, print_mess
    match = re.search(r'\d{2}/\d{2}$', media['caption'])
    chat_id, msg_id = m.chat.id, m.message_id
    if match:
        gallery = json.dumps(media)
        date = match[0]
        print('save_gallery', media, match, gallery)
        sql = "INSERT INTO message (msg_id, msg_chat_id, media, date) VALUES (%s, %s, %s, %s)"
        val = (msg_id, chat_id, gallery, date)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        print_mess(chat_id, 'Введіть дату')
    media = {
        'g_id': None,
        'media_list': [],
        'caption': ''
    }

for m in ml:
    m_handler(m)