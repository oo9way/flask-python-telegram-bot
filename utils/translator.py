import openai
import contants
import json


def translate_text(text, target_language):
    languages = contants.LANGUAGES
    langs = ", ".join(x[1] for x in languages.items() if x[0] != target_language)
    lang_keys = ", ".join(x[0] for x in languages.items() if x[0] != target_language)

    openai.api_key = contants.OPENAI_API_KEY
    prompt = f"""Translate the following text to {langs} and return text as only just json format. I do not need something else.
                Please do not return any other text and 
                original text. Keys should be language code and translation in value:\n\n{text}. Only {lang_keys} should be returned"""

    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )

            translated_text = response['choices'][0]['message']['content'].strip()
            result = json.loads(str(translated_text))
            break
        except Exception as e:
            print(e)
            continue
    return result