import re
import json
import logging

import telegram
from telegram.ext import ( Updater, CommandHandler, MessageHandler, Filters )

from constants import TOKEN
import custom_filters
import albums
import message
from db import mycursor, connection

# logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


# bot entities
bot = telegram.Bot(TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
   context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm bot. How can I help you?")

def print_albums(update, context):
   mycursor.execute("SELECT * FROM media")
   result = mycursor.fetchall()

   for m_id, media_group_id, files in result:
      print(f'printing album: {m_id} {media_group_id}')
      albums.send_album(update.effective_chat.id, json.loads(files), context)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('print_albums', print_albums))
dispatcher.add_handler(MessageHandler(Filters.text, message.handle_text))
dispatcher.add_handler(MessageHandler(custom_filters.album, albums.collect_album_items))
dispatcher.add_handler(MessageHandler(custom_filters.media, message.handle_media))

updater.start_polling()