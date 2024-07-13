from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot.')


def help_me(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start command")
