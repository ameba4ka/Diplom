from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from message import KEYBOARD_TEXT

back_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

back_kb.add(KeyboardButton(KEYBOARD_TEXT['back']))
