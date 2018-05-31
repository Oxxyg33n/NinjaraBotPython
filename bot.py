# Imports
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os

# Functions for handlers
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

# Initialize updater and dispatcher
updater = Updater(token=os.environ['NINJARA_TELEGRAMTOKEN'])
dispatcher = updater.dispatcher

# Handlers
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)

# Dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

# Set logging information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Start bot
updater.start_polling()
