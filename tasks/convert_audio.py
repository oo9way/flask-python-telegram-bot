from celery import shared_task
from data.models import Script
import requests
import json
from django.core.files.base import ContentFile
import base64


@shared_task
def convert_audio_task(script_id: int) -> None:
    script = Script.objects.get(id=script_id)

    post_data = {
        "voiceService": "servicebin",
        "voiceID": "uz-UZ2",
        "voiceSpeed": "0",
        "text": script.text_uz
    }

    headers = {
        "apikey": "TumnQA2gCzCPzIMehUclOZJWkDIxWeia",
        "content-type": "application/json"
    }

    response = requests.post(
        "https://ttsfree.com/api/v1/tts",
        headers=headers,
        data=json.dumps(post_data)
    )

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Error: {response.text}")
    else:
        data = response.json()
        wave_mp3 = base64.b64decode(data['audioData'])

        script.audio_uz.save('output.mp3', ContentFile(wave_mp3))
        script.save()

        print(f"Audio file saved with ID: {script.id}")

    post_data = {
        "voiceService": "servicebin",
        "voiceID": "ar-SA",
        "voiceSpeed": "0",
        "text": script.text_ar
    }

    response = requests.post(
        "https://ttsfree.com/api/v1/tts",
        headers=headers,
        data=json.dumps(post_data)
    )

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Error: {response.text}")
    else:
        data = response.json()
        wave_mp3 = base64.b64decode(data['audioData'])

        script.audio_ar.save('output.mp3', ContentFile(wave_mp3))
        script.save()

        print(f"Audio file saved with ID: {script.id}")

    post_data = {
        "voiceService": "servicebin",
        "voiceID": "ru-RU",
        "voiceSpeed": "0",
        "text": script.text_ru
    }

    response = requests.post(
        "https://ttsfree.com/api/v1/tts",
        headers=headers,
        data=json.dumps(post_data)
    )

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Error: {response.text}")
    else:
        data = response.json()
        wave_mp3 = base64.b64decode(data['audioData'])

        script.audio_ru.save('output.mp3', ContentFile(wave_mp3))
        script.save()

        print(f"Audio file saved with ID: {script.id}")


