import re
import json
import logging

import telegram
from telegram.ext import ( Updater, CommandHandler, MessageHandler, Filters )

from config import TOKEN
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

def help_handler(update, contenxt):
   text = "/hw or /homework - дізнатися домашку на сьогодні\n/tutorial - дізнатися, як працює бот"
   contenxt.bot.send_message(update.effective_chat.id, text)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_handler))
dispatcher.add_handler(MessageHandler(Filters.regex(r'\s*\d{2}[-\.\/]\d{2}\s*'), message.print_homework))
dispatcher.add_handler(MessageHandler(Filters.text, message.handle_text))
dispatcher.add_handler(MessageHandler(custom_filters.album, albums.collect_album_items))
dispatcher.add_handler(MessageHandler(custom_filters.media, message.handle_media))

updater.start_polling()