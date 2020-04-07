from db import mycursor, connection
import json
from telegram import InputMedia, InputMediaPhoto, InputMediaVideo
from telegram.ext import DispatcherHandlerStop
from telegram import ChatAction
from telegram import ParseMode


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
		ALBUM_DICT[media_group_id] = [update]
		# schedule the job
		context.job_queue.run_once(save_album, 1, context=[media_group_id])
	else:
		ALBUM_DICT[media_group_id].append(update)


def save_album(context):
	media_group_id = context.job.context[0]
	updates = ALBUM_DICT[media_group_id]

	# delete from ALBUM_DICT
	del ALBUM_DICT[media_group_id]

	files = []
	for update in updates:
		if update.message.photo:
			file_id = update.message.photo[-1].file_id
			caption = update.message.caption
			files.append({
				'type': 'photo',
				'file_id': file_id,
				'caption': caption
			})
		elif update.message.video:
			file_id = update.message.video.file_id
			caption = update.message.caption
			files.append({
				'type': 'video',
				'file_id': file_id,
				'caption': caption
			})

	sql = "INSERT INTO media (media_group_id, files) VALUES (%s, %s)"
	val = (media_group_id, json.dumps(files))
	mycursor.execute(sql, val)
	connection.commit()


