from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from message import KEYBOARD_TEXT

class LiquidStatsKeyboard:
    def get_keyboard(self):
        button_hourly = KeyboardButton(KEYBOARD_TEXT.get('hourly'))
        button_total = KeyboardButton(KEYBOARD_TEXT.get('total'))
        button_back = KeyboardButton(KEYBOARD_TEXT.get('back'))
        # button_balance = KeyboardButton(KEYBOARD_TEXT.get('balance'))

        start_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_hourly, button_total).row(button_back)
        return start_kb