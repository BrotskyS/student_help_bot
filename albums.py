from db import mycursor, connection
from utils import find_date
import json
from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction

ALBUM_DICT = {}


def collect_album_items(update, context):
	"""
	if album is edited:
		- check if it saved as homework:
			if yes: update saved caption
			else: if valid date is specified - save as homework

	In other case:
		if the media_group_id not a key in the dictionary yet:
			- send sending action
			- create a key in the dict with media_group_id
			- add a list to the key and the first element is this update
			- schedule a job in 1 sec
		else:
			- add update to the list of that media_group_id
	"""
	
	if update.edited_message:
		message = update.edited_message

		update_album_caption(message.media_group_id, message.message_id, message.caption)

		mycursor.execute(f'SELECT COUNT(id) FROM homework WHERE media_group_id = {message.media_group_id}')
		count = mycursor.fetchone()[0]

		if count == 0:
			date = find_date(message.caption)
			if date:
				save_album_homework(message.from_user.id, message.chat.id, message.media_group_id, date)

		return

	# collecting album items 
	media_group_id = update.message.media_group_id
	if media_group_id not in ALBUM_DICT:
		context.bot.sendChatAction(
			chat_id=update.message.from_user.id,
			action=ChatAction.UPLOAD_PHOTO if update.message.photo else ChatAction.UPLOAD_VIDEO
		)
		ALBUM_DICT[media_group_id] = {
			'updates': [update],
			'caption': update.message.caption
		}
		# schedule the job
		context.job_queue.run_once(save_album, 1, context=[media_group_id])
	else:
		ALBUM_DICT[media_group_id]['updates'].append(update)


def save_album(context):
	media_group_id = context.job.context[0]
	updates, caption = ALBUM_DICT[media_group_id]['updates'], ALBUM_DICT[media_group_id]['caption']
	user_id, from_chat_id = updates[0].message.from_user.id, updates[0].message.chat.id

	# delete from ALBUM_DICT
	del ALBUM_DICT[media_group_id]

	files = []
	for update in updates:
		if update.message.photo:
			file_id = update.message.photo[-1].file_id
			files.append(
				{
					'message_id': update.message.message_id,
					'type': 'photo',
					'file_id': file_id,
					'caption': update.message.caption
				}
			)
		elif update.message.video:
			file_id = update.message.video.file_id
			files.append(
				{
					'message_id': update.message.message_id,
					'type': 'video',
					'file_id': file_id,
					'caption': update.message.caption
				}
			)

	sql = "INSERT INTO media (media_group_id, files) VALUES (%s, %s)"
	val = (media_group_id, json.dumps(files))
	mycursor.execute(sql, val)
	connection.commit()

	# Save as homework
	date = find_date(caption)
	if date:
		save_album_homework(user_id, from_chat_id, media_group_id, date)
	else:
		pass
		# context.bot.send_message(from_chat_id, 'Вкажіть коректну дату дз')

def save_album_homework(user_id, from_chat_id, media_group_id, date):
	sql = "INSERT INTO homework (user_id, from_chat_id, media_group_id, date) VALUES (%s, %s, %s, %s)"
	val = (user_id, from_chat_id, media_group_id, date)
	mycursor.execute(sql, val)
	connection.commit()

def update_album_caption(media_group_id, message_id, new_caption):
	# get album data
	mycursor.execute(f"SELECT files FROM media WHERE media_group_id = '{media_group_id}'")
	result = mycursor.fetchone()
	
	if result:
		album_files = json.loads(result[0])

		for i in range(len(album_files)):
			if album_files[i]['message_id'] == message_id:
				album_files[i]['caption'] = new_caption
				break
		
		# save changes to database
		sql = "UPDATE media SET files = %s WHERE media_group_id = %s"
		val = (json.dumps(album_files), media_group_id)
		mycursor.execute(sql, val)
		connection.commit()

	else:
		print('Album to update don\'t exist')
		return

def send_album(chat_id, files, context):

	# ordering album files
	files.sort(key=lambda f: f['message_id'])

	media = []
	for f in files:
		if f['type'] == 'photo':
			media.append(
				InputMediaPhoto(
					media=f['file_id'],
					caption=f['caption'],
				)
			)
		elif f['type'] == 'video':
			media.append(
				InputMediaVideo(
					media=f['file_id'],
					caption=f['caption'],
				)
			)

	context.bot.sendMediaGroup(
		chat_id=chat_id,
		media=media
	)
