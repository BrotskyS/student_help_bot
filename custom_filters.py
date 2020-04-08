from telegram.ext import BaseFilter, Filters

class Album(BaseFilter):
	def filter(self, message):
		if (message.photo or message.video) and message.media_group_id is not None:
			return True

album = Album()

# filter for media which is not an album
media = (Filters.photo | Filters.audio | Filters.document) & (~ album)