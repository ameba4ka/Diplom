from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from message import KEYBOARD_TEXT


class StartKeyboard:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_button_stats(self):
        return KeyboardButton(KEYBOARD_TEXT.get('statistic'))
    
    def get_button_liquid(self):
        return KeyboardButton(KEYBOARD_TEXT.get('add_liquid'))
    
    def get_button_meta(self):
        return KeyboardButton(KEYBOARD_TEXT.get('meta'))

    def get_keyboard(self):
        button_stats = self.get_button_stats()
        button_liquid = self.get_button_liquid()
        button_meta = self.get_button_meta()

        start_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_stats, button_liquid).add(button_meta)
        return start_kb
