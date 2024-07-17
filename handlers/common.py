from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

import states as st
from keyboards import replies
from data.models import Script
from tasks.create_script import translate_task
from tasks.convert_audio import convert_audio_task


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
        context.user_data["language"] = "ar"
        text = "لقد اخترت اللغة العربية.\nأرسل نص"

    else:
        context.user_data["language"] = "ar"
        text = "Mavjud bo'lmagan til tanlandi. Iltimos berilgan tugmalar orqali tilni tanlang.\n"
        text += "تم تحديد لغة غير متاحة. الرجاء تحديد لغة باستخدام الأزرار المتوفرة."
        update.message.reply_text(text, reply_markup=replies.language_keyboard())
        return st.LANGUAGE

    update.message.reply_text(text, reply_markup=replies.back_keyboard())
    return st.SCRIPT


def get_script(update: Update, context: CallbackContext):
    text = update.message.text
    if text.startswith("Ortga") or text.startswith("رجع"):
        message = "Bosh menyuga qaytildi.\n"
        message += "القائمة الرئيسية"
        update.message.reply_text(message, reply_markup=replies.home_keyboard())
        return st.HOME

    script = Script.objects.create(text=text, language=context.user_data["language"])
    context.user_data["last_script_id"] = script.id
    message = "Matn saqlandi. Tarjima jarayoni boshlandi ...\n"
    message += "تم حفظ النص. بدأت عملية الترجمة..."
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    translate_task.apply_async(
        args=[text, context.user_data["language"], update.message.chat_id, script.id],
        countdown=2
    )
    return st.TRANSLATION_JOB


def get_list(update: Update, context: CallbackContext):
    language = update.message.text
    if language.startswith("O'zbek"):
        language = "uz"

    elif language.startswith("Arabic"):
        language = "ar"

    elif language.startswith("Russian"):
        language = "ru"

    else:
        message = "Mavjud bo'lmagan til tanlandi. Iltimos berilgan tugmalar orqali tilni tanlang.\n"
        message += "تم اختيار لغة غير متاحة. الرجاء تحديد اللغة باستخدام الأزرار المتوفرة"
        update.message.reply_text(message, reply_markup=replies.language_keyboard())
        return st.LIST
    
    filter = {
        f"text_{language}__isnull": False,
        "is_approved": True
    }
    scripts = Script.objects.filter(**filter)
    if len(scripts) == 0:
        message = "Hech qanday matn mavjud emas.\n"
        message += "لم يتم العثور على نص"
        update.message.reply_text(message, reply_markup=replies.home_keyboard())
        return st.HOME

    message = "Matnlar ro'yxati / قائمة النصوص\n"
    for script in scripts:
        message += f'<a href="https://almadina.joseph.uz/details/{script.id}">{script.created_at.strftime("%-d %B, %Y")}</a>\n'
    update.message.reply_text(message, reply_markup=replies.home_keyboard(), parse_mode='html')
    return st.HOME


def get_translation(update: Update, context: CallbackContext):
    text = update.message.text
    if text.startswith("Tarjimani o'zgartirish / تحرير الترجمة"):
        message = "Qaysi tildagi tarjimani o'zgartirmoqchisiz ?\n"
        message += "ما هي الترجمة التي تريد تغييرها؟"
        update.message.reply_text(message, reply_markup=replies.translation_languages_keyboard())
        return st.EDIT_TRANSLATION_TEXT

    if text.startswith("Tarjimani tasdiqlash / تأكيد الترجمة"):
        script_id = context.user_data["last_script_id"]
        script = Script.objects.get(id=script_id)
        script.is_approved = True
        script.save(update_fields=["is_approved"])
        message = "Tarjimani tasdiqlandi.\n"
        message += "تم تأكيد الترجمة"

        convert_audio_task.apply_async(args=[script_id], countdown=2)
        del context.user_data["last_script_id"]
        update.message.reply_text(message, reply_markup=replies.home_keyboard())
        return st.HOME

    message = "Noto'g'ri buyruq yuborildi. Iltimos, kerakli tugmani tanlang.\n"
    message += "تم إرسال أمر غير صالح. الرجاء تحديد الزر المطلوب."

    update.message.reply_text(message, reply_markup=replies.confirm_or_edit_keyboard())
    return st.TRANSLATION_CONFIRM


def get_translation_edit_language(update: Update, context: CallbackContext):
    text = update.message.text
    message = None

    if text.startswith("O'zbek"):
        message = "O'zbek tilidagi tarjimani yuboring \nأرسل الترجمة الأوزبكية"
        context.user_data["editing_language"] = "uz"
    elif text.startswith("Arabic"):
        message = "Arabic tilidagi tarjimani yuboring \nأرسل الترجمة العربية"
        context.user_data["editing_language"] = "ar"
    elif text.startswith("Russian"):
        message = "Rus tilidagi tarjimani yuboring \nأرسل الترجمة الروسية"
        context.user_data["editing_language"] = "ru"

    if context.user_data.get("editing_language", None) is not None and message:
        update.message.reply_text(message, reply_markup=replies.back_keyboard())
        return st.SAVE_EDITED_TRANSLATION
    
    message = "Noto'g'ri buyruq yuborildi. Iltimos, kerakli tugmani tanlang.\n"
    message += "تم إرسال أمر غير صالح. الرجاء تحديد الزر المطلوب."

    update.message.reply_text(message, reply_markup=replies.translation_languages_keyboard())
    return st.EDIT_TRANSLATION_TEXT


def save_edited_translation(update: Update, context: CallbackContext):
    text = update.message.text
    script = Script.objects.get(id=context.user_data["last_script_id"])

    if text.startswith("Ortga") or text.startswith("رجع"):
        message = "**Translated scripts:**\n\n"
        message += f"O'zbek: {script.text_uz}\n\n"
        message += f"Arabic: {script.text_ar}\n\n"
        message += f"Russian: {script.text_ru}\n\n"
        update.message.reply_text(message, reply_markup=replies.confirm_or_edit_keyboard())
        return st.TRANSLATION_JOB

    else:
        if context.user_data["editing_language"] == "uz":
            script.text_uz = text

        if context.user_data["editing_language"] == "ar":
            script.text_ar = text

        if context.user_data["editing_language"] == "ru":
            script.text_ru = text
        
        script.save()
        
        message = "**Translated scripts:**\n\n"
        message += f"O'zbek: {script.text_uz}\n\n"
        message += f"Arabic: {script.text_ar}\n\n"
        message += f"Russian: {script.text_ru}\n\n"
        update.message.reply_text(message, reply_markup=replies.confirm_or_edit_keyboard())
        return st.TRANSLATION_JOB

