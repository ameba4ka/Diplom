from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from message import KEYBOARD_TEXT

class AddLiquidKeyboard:
    
    def get_buttons(self):
        button_water = InlineKeyboardButton(KEYBOARD_TEXT.get('water'), callback_data="liq_water")
        button_juice = InlineKeyboardButton(KEYBOARD_TEXT.get('juice'), callback_data="liq_juice")
        button_alcohol = InlineKeyboardButton(KEYBOARD_TEXT.get('alcohol'), callback_data="liq_alcohol")
        button_sparkling_water = InlineKeyboardButton(KEYBOARD_TEXT.get('sparkling_water'), callback_data="liq_sparkling_water")
        button_coffee = InlineKeyboardButton(KEYBOARD_TEXT.get('coffee'), callback_data="liq_coffee")
        button_tea = InlineKeyboardButton(KEYBOARD_TEXT.get('tea'), callback_data="liq_tea")
        button_milk = InlineKeyboardButton(KEYBOARD_TEXT.get('milk'), callback_data="liq_milk")

        return [button_water, button_juice, button_alcohol, button_sparkling_water, button_coffee, button_tea, button_milk]

    def get_keyboard(self):
        buttons = self.get_buttons()

        add_liquid_kb = InlineKeyboardMarkup(resize_keyboard=True).add(*buttons)

        return add_liquid_kb
