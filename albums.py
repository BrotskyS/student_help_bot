from db import mycursor, connection
from constants import date_pattern
import json
from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction

ALBUM_DICT = {}


def collect_album_items(update, context):
	"""
	if the media_group_id not a key in the dictionary yet:
		- send sending action
		- create a key in the dict with media_group_id
		- add a list to the key and the first element is this update
		- schedule a job in 1 sec
	else:
		- add update to the list of that media_group_id
	"""
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

	match = date_pattern.search(caption)
	if match:

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

		save_album_homework(user_id, from_chat_id, media_group_id, match[1])
	else:
		context.bot.send_message(from_chat_id, 'Вкажіть коректну дату дз')

def save_album_homework(user_id, from_chat_id, media_group_id, date):
	sql = "INSERT INTO homework (user_id, from_chat_id, media_group_id, date) VALUES (%s, %s, %s, %s)"
	val = (user_id, from_chat_id, media_group_id, date)
	mycursor.execute(sql, val)
	connection.commit()

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
