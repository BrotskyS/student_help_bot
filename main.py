import re
import logging

import telegram
from telegram.ext import ( Updater, CommandHandler, MessageHandler, Filters )

import custom_filters
import albums

# logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# basic variables and constants
TOKEN = '1009237691:AAGbCBSJAYBjVMruuTSCFAmNKRKYScvJ6aA'
date_pattern = re.compile(r'(\d{2}/\d{2})(?:\s+)?$')

# bot entites
bot = telegram.Bot(TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
   context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm bot. How can I help you?")


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(custom_filters.album, albums.collect_album_items))

updater.start_polling()