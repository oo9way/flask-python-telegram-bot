from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, ConversationHandler, MessageHandler, Filters

import contants
import states as st
from handlers import common, commands

bot = Bot(token=contants.BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

dispatcher.add_handler(ConversationHandler(
    entry_points=[CommandHandler('start', commands.start)],
    states={
        st.HOME: [MessageHandler(Filters.text, common.home)],
        st.LANGUAGE: [MessageHandler(Filters.text, common.get_language)],
        st.SCRIPT: [MessageHandler(Filters.text, common.get_script)],
        st.LIST: [MessageHandler(Filters.text, common.get_list)],
        # st: [MessageHandler(Filters.photo, onboarding_handlers.accept_check)],
    },
    fallbacks=[common.error],
))

dispatcher.add_handler(CommandHandler("help", commands.help_me))
dispatcher.add_error_handler(common.error)
