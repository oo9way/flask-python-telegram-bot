from celery import shared_task
from utils.translator import translate_text
from data.models import Script
from keyboards import replies
import requests


@shared_task
def translate_task(text: str, target_language: str, chat_id: int, script_id) -> None:
    from dispatcher import bot
    script = Script.objects.get(id=script_id)

    if target_language == "uz":
        url = f'https://mal1kov.uz/lotin-kirill-api/latin'
        headers = {'Content-Type': 'application/json'}
        data = {'text': text}

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            text = response.json()['result']

    result = translate_text(text, target_language)
    texts = result
    texts[target_language] = text
    script.text_ar = texts['ar']
    script.text_uz = texts['uz']
    script.text_ru = texts['ru']
    script.save()

    message = "**Translated scripts:**\n\n"
    for language, text in texts.items():
        message += f"{language}: {text}\n\n"

    bot.send_message(chat_id=chat_id, text=message, reply_markup=replies.confirm_or_edit_keyboard())
