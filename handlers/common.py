from telegram import Update
from telegram.ext import CallbackContext

import states as st
from keyboards import replies
from data.models import Script


def error(update: Update, context: CallbackContext):
    update.message.reply_text("We have got an error while processing your request. We are working on it.")


def home(update: Update, context: CallbackContext):
    text = update.message.text
    if text == "Matn qo'shish / أضف نصًا":
        message = "Matn qo'shish uchun tilni tanlang\n"
        message += "لإضافة نص، يرجى اختيار اللغة من قبل"
        update.message.reply_text(message, reply_markup=replies.language_keyboard())
        return st.LANGUAGE

    if text == "Qo'shilgan matnlar / النصوص المضافة":
        message = "Qaysi tilda olmoqchisiz ?\n"
        message += "ما هي اللغة التي تريد أن تأخذها؟"
        update.message.reply_text(message, reply_markup=replies.language_keyboard())
        return st.LIST

    message = "Noto'g'ri buyruq yuborildi. Iltimos, kerakli tugmani tanlang.\n"
    message += "أمر غير صالح. الرجاء اختيار أحد الأزرار"

    update.message.reply_text(message, reply_markup=replies.home_keyboard())
    return st.HOME


def get_language(update: Update, context: CallbackContext):
    language = update.message.text
    if language.startswith("O'zbek"):
        context.user_data["language"] = "uz"
        text = "Siz o'zbek tilini tanladingiz.\nMatnni yuboring."

    elif language.startswith("Arabic"):
        text = "لقد اخترت اللغة العربية.\nأرسل نص"

    else:
        context.user_data["language"] = "ar"
        text = "Mavjud bo'lmagan til tanlandi. Iltimos berilgan tugmalar orqali tilni tanlang.\n"
        text += "تم تحديد لغة غير متاحة. الرجاء تحديد لغة باستخدام الأزرار المتوفرة."
        update.message.reply_text(text, reply_markup=replies.home_keyboard())
        return st.LANGUAGE

    update.message.reply_text(text, reply_markup=replies.back_keyboard())
    return st.SCRIPT


def get_script(update: Update, context: CallbackContext):
    text = update.message.text
    if text.startswith("Ortga") or text.startswith("رجع"):
        message = "Ortga qaytildi. Davom etish uchun tilni tanlang\n"
        message += "لمواصلة العملية اختر اللغة"
        update.message.reply_text(message, reply_markup=replies.home_keyboard())
        return st.LANGUAGE

    Script.objects.create(text=text, language=context.user_data["language"])
    message = "Matn saqlandi. Tarjima jarayoni boshlandi ...\n"
    message += "تم حفظ النص. بدأت عملية الترجمة..."
    update.message.reply_text(message, reply_markup=replies.home_keyboard())
    return st.HOME


def get_list(update: Update, context: CallbackContext):
    language = update.message.text
    if language.startswith("O'zbek"):
        language = "uz"

    elif language.startswith("Arabic"):
        language = "ar"

    else:
        message = "Mavjud bo'lmagan til tanlandi. Iltimos berilgan tugmalar orqali tilni tanlang.\n"
        message += "تم اختيار لغة غير متاحة. الرجاء تحديد اللغة باستخدام الأزرار المتوفرة"
        update.message.reply_text(message, reply_markup=replies.language_keyboard())
        return st.LIST

    scripts = Script.objects.filter(language=language)
    if len(scripts) == 0:
        message = "Hech qanday matn mavjud emas.\n"
        message += "لم يتم العثور على نص"
        update.message.reply_text(message, reply_markup=replies.home_keyboard())
        return st.HOME

    message = "Malumot topildi"
    update.message.reply_text(message, reply_markup=replies.home_keyboard())
    return st.HOME