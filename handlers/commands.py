from telegram import Update
from telegram.ext import CallbackContext
from keyboards import replies
import states as st


def start(update: Update, context: CallbackContext) -> None:
    message = "Assalamu alaykum, botga xush kelibsiz\n"
    message += "السَّلاَمُ عَلَيْكُمْ, مرحبا بكم في بوت"
    update.message.reply_text(message, reply_markup=replies.home_keyboard())
    return st.HOME


def help_me(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start command")
