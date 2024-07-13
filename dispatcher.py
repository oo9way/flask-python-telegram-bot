from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler

import contants
from handlers import common, commands

bot = Bot(token=contants.BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

dispatcher.add_handler(CommandHandler("start", commands.start))
dispatcher.add_handler(CommandHandler("help", commands.help_me))

dispatcher.add_error_handler(common.error)
