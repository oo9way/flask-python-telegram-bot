from telegram import Update
from telegram.ext import CallbackContext


def error(update: Update, context: CallbackContext):
    update.message.reply_text("We have got an error while processing your request. We are working on it.")