from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from message import KEYBOARD_TEXT

class MetaKeyboard:
    def get_keyboard(self):
        button_update = KeyboardButton(KEYBOARD_TEXT.get('update_meta'))
        button_meta_info = KeyboardButton(KEYBOARD_TEXT.get('meta_info'))
        button_back = KeyboardButton(KEYBOARD_TEXT.get('back'))

        start_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_update, button_meta_info).row(button_back)
        return start_kb