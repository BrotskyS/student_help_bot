from db import mycursor, connection
from utils import find_date
from albums import send_album
import json
import re

def handle_text(update, context):
# try:
	print('<INCOMING MESSAGE:\n')
	chat_id = update.effective_chat.id

	text = update.message.text #text = update.message.text if update.message.text else update.message.caption
	match = re.search(r'^(?:\s+)?(дз)?(?:.*)(\d{2}/\d{2})(?:\s+)?$', text, re.I)
	
	if match:
		date = match[2]
		if match[1]:
			print('Handle printing homework\n')
			print_homework(chat_id, date, context)
		else:
			print('Handle adding homework\n')
			save_homework(update.message, date, context)
	else:
		print('Invalid message format\n')
		context.bot.send_message(chat_id, 'Вкажіть дату ДЗ')

	print('\nEND MESSAGE>\n\n')
# except:
# 	context.bot.send_message(chat_id, 'Ой, щось поломалося, "handle_text" ')


def handle_media(update, context):
#try:
	print('<INCOMING MEDIA:\n')
	chat_id = update.effective_chat.id
	text = update.message.caption

	date = find_date(text)
	if date:
		print('Handle adding homework\n')
		save_homework(update.message, date, context)
	else:
		context.bot.send_message(chat_id, 'Вкажіть дату ДЗ')

	print('\nEND MEDIA>\n\n')
# except:
# 	context.bot.send_message(chat_id, 'Ой, щось поломалося, "handle_text" ')

def print_homework(chat_id, date, context):
	print('print_homework')
	try:
		mycursor.execute(f"SELECT message_id, from_chat_id, media_group_id FROM homework WHERE date = '{date}'")
		myresult = mycursor.fetchall()

		if len(myresult) == 0:
			context.bot.send_message(chat_id, 'Немає ДЗ на вказану дату')
			return
		
		for message_id, from_chat_id, media_group_id in myresult:
			
			if media_group_id != None:
				mycursor.execute(f"SELECT * FROM media WHERE media_group_id = '{media_group_id}'")
				result = mycursor.fetchall()

				for m_id, media_group_id, files in result:
					print(f'printing album: {m_id} {media_group_id}')
					send_album(chat_id, json.loads(files), context)
			else:
				context.bot.forward_message(chat_id, from_chat_id, message_id)

	except:
		context.bot.send_message(chat_id, 'Ой, щось поломалося (print_homework)')

def save_homework(m, date, context):
	print('add_homework')

# try:
	sql = "INSERT INTO homework (message_id, from_chat_id, user_id, date) VALUES (%s, %s, %s, %s)"
	val = (m.message_id, m.chat.id, m.from_user.id, date)
	mycursor.execute(sql, val)
	connection.commit()
# except:
	# context.bot.send_message(m.chat.id, 'Ой, щось поломалося (save_homework)')