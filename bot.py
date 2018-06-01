# Imports
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
import tweepy

# Set access keys
auth = tweepy.OAuthHandler('pOd1glTyWGWUvqpxDm1E6D1Ld','VNtlTjULQ7RPMvEiSRA1fqgxvsYAAD5TbYyN30e5mEzN5LWXkO')
auth.set_access_token('928074244608659459-LVI3awgqk7QOyBzlykiLxBrOlfw7fOt','NM6UetE6krex4q6yIjLz94mVEGwFzcwRJdGJXIwipvPIX')

# Create API object
api = tweepy.API(auth)

# Functions for handlers
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Hi, I'm Ninjara Bot written in Python as an exam project!")
	bot.send_message(chat_id=update.message.chat_id, text="Bot has been done by Aleksandr Logvinenko for ICS0015 course")
	bot.send_message(chat_id=update.message.chat_id, text="Github repository link: https://github.com/Oxxyg33n/NinjaraBotPython")
	bot.send_message(chat_id=update.message.chat_id, text="To get a list of available commands, write /help")

def echo(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="You said something to me ("+update.message.text+"), but I don't understand you!")
	bot.send_message(chat_id=update.message.chat_id, text="Please, enter /help to get a list of available commands")

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand your command")
	help(bot, update)

def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="To use me, enter one of the following commands: ")
	bot.send_message(chat_id=update.message.chat_id, text="/timeline will print out home timeline of user Oxxy_wtf")
	bot.send_message(chat_id=update.message.chat_id, text="/post <message> will post message to my page")
	bot.send_message(chat_id=update.message.chat_id, text="/friends will print out my twitter's friend list")
	bot.send_message(chat_id=update.message.chat_id, etxt="/search <query> to search latest 10 posts with given query")

def get_home_timeline(bot, update):
	public_tweets = api.home_timeline()
	for tweet in public_tweets:
		bot.send_message(chat_id=update.message.chat_id, text=tweet.text)
		bot.send_message(chat_id=update.message.chat_id, text="-----------------------------------")

def get_followers(bot, update):
	user = api.get_user('oxxy_wtf')
	print(user.friends())
	if(user.friends() != []):
		for friend in user.friends():
			bot.send_message(chat_id=update.message.chat_id, text="Oxxy's friends: ")
			bot.send_message(chat_id=update.message.chat_id, text=friend.screen_name)
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Currently Oxxy doesn't have any friends :(")

def post_to_timeline(bot, update, args):
	text_to_post = ' '.join(args)
	api.update_status(text_to_post)

def search_string(bot, update, args):
	max_tweets = 10 # Set bot to search only 10 latest tweets
	if(args == []):
		args = 'Nintendo'
		bot.send_message(chat_id=update.message.chat_id, text="You forgot to enter query to search for")
		bot.send_message(chat_id=update.message.chat_id, text="Defaulting to Nintendo")
	text_to_search = ' '.join(args)
	searched_tweets = api.search(q=text_to_search, count = max_tweets)

	for tweet in searched_tweets:
		bot.send_message(chat_id=update.message.chat_id, text='@'+tweet.user.screen_name)
		bot.send_message(chat_id=update.message.chat_id, text=tweet.text)
		bot.send_message(chat_id=update.message.chat_id, text="-----------------------------------")
	

# Initialize updater and dispatcher
updater = Updater(token=os.environ['NINJARA_TELEGRAMTOKEN'])
dispatcher = updater.dispatcher

# Handlers
start_handler = CommandHandler('start', start)
get_followers_handler = CommandHandler('friends', get_followers)
timeline_handler = CommandHandler('timeline', get_home_timeline)
ptt_handler = CommandHandler('post', post_to_timeline, pass_args=True)
search_handler = CommandHandler('search', search_string, pass_args=True)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)

# Dispatchers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(timeline_handler)
dispatcher.add_handler(get_followers_handler)
dispatcher.add_handler(ptt_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(unknown_handler)

# Set logging information
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Start bot
updater.start_polling()
