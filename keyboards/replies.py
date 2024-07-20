from telegram import ReplyKeyboardMarkup, KeyboardButton
from django.core.cache import cache


def make_keyboard(keyboards, **kwargs):
    mock_keyboard = []
    for keyboard in keyboards:
        if isinstance(keyboard, dict):
            mock_keyboard.append([
                KeyboardButton(text=keyboard.get("text"), **keyboard.get("params", {}))
            ])
        else:
            buttons = []
            for button in keyboard:
                buttons.append(
                    KeyboardButton(text=button.get("text"), **button.get("params", {}))
                )
            mock_keyboard.append(buttons)

    return ReplyKeyboardMarkup(keyboard=mock_keyboard, **kwargs)


def home_keyboard():
    keyboards = [
        [
            {"text": "Matn qo'shish / أضف نصًا"},
            {"text": "Qo'shilgan matnlar / النصوص المضافة"},
            {"text": "Matnni o'zgartirish / تغيير البرنامج النصي"}

        ]
    ]
    return make_keyboard(keyboards, resize_keyboard=True)


def language_keyboard():
    keyboards = [
        [
            {"text": "O'zbek tili"},
            {"text": "Arabic"}
        ]
    ]
    return make_keyboard(keyboards, resize_keyboard=True)


def back_keyboard():
    keyboards = [
        [{"text": "Ortga"}, {"text": "رجع"}]
    ]
    return make_keyboard(keyboards, resize_keyboard=True)


def confirm_or_edit_keyboard():
    keyboards = [
        [
            {"text": "Tarjimani o'zgartirish / تحرير الترجمة"},
            {"text": "Tarjimani tasdiqlash / تأكيد الترجمة"},
        ]
    ]

    return make_keyboard(keyboards, resize_keyboard=True)


def translation_languages_keyboard():
    keyboards = [
        [
            {"text": "O'zbek"},
            {"text": "Arabic"},
            {"text": "Russian"},
        ]
    ]
    return make_keyboard(keyboards, resize_keyboard=True)


def enum_keyboard(n):
    keyboards = [[{"text": "Ortga"}, {"text": "رجع"}], []]

    for i in range(n):
        keyboards[1].append(
            {"text": str(i + 1)}
        )

    return make_keyboard(keyboards, resize_keyboard=True)
