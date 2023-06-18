import logging
import pandas as pd
import asyncio
from reminders.daily import DailyWaterReminder

import logging

from aiogram import types
from aiogram.dispatcher import filters
from db.utils import execute_query
from db.user import insert_user
from db import db,cursor
from db.liquid import insert_liquid_intake
from message import KEYBOARD_TEXT
from kb.start_keyboard import StartKeyboard
from kb.meta import MetaKeyboard
from kb.add_liquid import AddLiquidKeyboard
from kb.liquid_statistic import LiquidStatsKeyboard
from kb.back import back_kb
from states.liquid_state import LiquidStates
from states.meta_state import MetaStates
from loader import dp, bot
from liquid_stats import info, trends, balance
from db.create import create_tables
from dotenv import load_dotenv
load_dotenv()


def generate_dataframe_from_mysql(user_id):
    query = """
        SELECT *
        FROM liquidIntake
        JOIN user ON liquidIntake.user_id = user.user_id
        WHERE liquidintake.user_id = %s;
        """

    # Execute the SQL query
    result = execute_query(query, user_id)

    # Create a DataFrame from the rows and column names
    df = pd.DataFrame.from_dict(result)
    return df



# Configure logging
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    user = message.from_user
    user_id = user.id
    username = user.username
    print(user_id)

    # Перевірка, чи користувач уже зареєстрований
    query = "SELECT * FROM User WHERE user_id = %s"
    result = execute_query(query, user_id)
    
    if not result:
        insert_user(user_id, username)

    # Відправка повідомлення з клавіатурою
    keyboard = StartKeyboard(user_id)


    await message.reply("Вітаю! Я бот для відстеження рідини, яку ви вживаєте. Що б ви хотіли зробити?", reply_markup=keyboard.get_keyboard())

# Обробка натискання на кнопку "Статистика"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('statistic')))
async def statistics(message: types.Message):
    await message.reply("Ось доступні для вас статистичні данні:", reply_markup=LiquidStatsKeyboard().get_keyboard())

# Обробка натискання на кнопку "Тренди Статистика"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('hourly')))
async def statistics_hourly(message: types.Message):
    user_id = message.from_user.id
    df = generate_dataframe_from_mysql(user_id)
    chart_buf = trends.create_trend(df)
    chart = types.InputFile(chart_buf, filename='result.png')
    # Відправка статистики
    await message.answer_photo(chart)


# Обробка натискання на кнопку "Загальна Статистика"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('total')))
async def statistics_total(message: types.Message):
    user_id = message.from_user.id
    # Отримання статистики
    result = info.get_formated_statistics(user_id)
    await message.reply(result)

# Обробка натискання на кнопку "Баланс Статистика"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('balance')))
async def statistics_total(message: types.Message):
    user_id = message.from_user.id
    df = generate_dataframe_from_mysql(user_id)
    # Отримання статистики
    result = balance.balance_liquid(df)
    await message.reply(result)

@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('back')))
async def back(message: types.Message):
    user_id = message.from_user.id
    await message.reply("Ви повернулись до головного меню", reply_markup=StartKeyboard(user_id).get_keyboard())


# Обробка натискання на кнопку "Додати рідину"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('add_liquid')))
async def add_liquid(message: types.Message):
    await message.reply("Оберіть тип рідини, яку ви вживаєте:", reply_markup=AddLiquidKeyboard().get_keyboard())


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('liq_'))
async def process_callback_liquid(callback_query: types.CallbackQuery):
    code = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id
    states = LiquidStates().all()
    state_idx = states.index(code)

    #set state
    state = dp.current_state(user=user_id)

    await state.set_state(LiquidStates().all()[state_idx])
    # Збереження типу рідини в контексті
    await callback_query.message.bot.send_message(chat_id=user_id, text=f"Введіть кількість вжитої рідини у мл для типу {KEYBOARD_TEXT.get(code)}:",reply_markup=back_kb)


@dp.message_handler(state=LiquidStates.all())
async def add_liquid_amount(message: types.Message):
    liquid = message.text
    user_id = message.from_user.id
    # Отримання типу рідини з контексту
    state = dp.current_state(user=user_id)
    liquid_type = await state.get_state()

    if message.text == KEYBOARD_TEXT['back']:
        await message.answer("Відміна додавання рідини", reply_markup=StartKeyboard(user_id).get_keyboard())
        await message.reply("Оберіть тип рідини, яку ви вживаєте:", reply_markup=AddLiquidKeyboard().get_keyboard())
        await state.reset_state()
        return

    if liquid.isdigit():
        try:
            amount = float(liquid)

            # Додавання запису про вжиту рідину
            insert_liquid_intake(user_id, liquid_type, amount)
            await state.reset_state()
            DailyWaterReminder().update_reminder(user_id)
            # Відправка повідомлення з підтвердженням
            await message.reply(f"Запис про вжиту рідину додано:\nТип: {KEYBOARD_TEXT.get(liquid_type)}\nКількість: {liquid} мл",reply_markup=StartKeyboard(user_id).get_keyboard())
        except ValueError:
            # Введено некоректне значення
            await message.reply("Некоректне значення. Будь ласка, введіть кількість у форматі числа.")
    else:
        # Введено некоректне повідомлення
        await message.reply("Некоректне повідомлення. Будь ласка, введіть кількість у форматі числа.")

# Обробка натискання на кнопку "Мета"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT['meta']))
async def meta(message: types.Message):
    user = message.from_user
    user_id = user.id
    states = MetaStates().all()
    state_idx = states.index('weight')
    # Перевірка, чи користувач уже зареєстрований
    query = "SELECT * FROM User WHERE user_id = %s"
    result = execute_query(query, user_id)
    if not result[0].get('weight'):
        await message.reply("Ви не зареєстровані. Будь ласка, введіть вашу вагу у кг:",reply_markup=MetaKeyboard().get_keyboard())
        state = dp.current_state(user=user_id)
        await state.set_state(MetaStates().all()[state_idx])
    await message.reply(f"Мета: {result[0]['water_meta_amount']} мл", reply_markup=MetaKeyboard().get_keyboard())



# Обробка натискання на кнопку "Оновлення Мети"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('update_meta')))
async def meta_update(message: types.Message):
    user = message.from_user
    user_id = user.id
    states = MetaStates().all()
    state_idx = states.index('weight')

    await message.reply("Будь ласка, введіть вашу вагу у кг:",reply_markup=MetaKeyboard().get_keyboard())
    state = dp.current_state(user=user_id)
    await state.set_state(MetaStates().all()[state_idx])


# Обробка натискання на кнопку "Моя Мета"
@dp.message_handler(filters.Text(equals=KEYBOARD_TEXT.get('meta_info')))
async def meta_info(message: types.Message):
    user = message.from_user
    user_id = user.id
    query = "SELECT * FROM User WHERE user_id = %s"
    result = execute_query(query, user_id)
    row = result[0]
    weight = row.get('weight')
    water_meta_amount = row.get('water_meta_amount')

    today_water = info.today_statistics(user_id)

    is_meta_accomplished = water_meta_amount <= today_water
    if is_meta_accomplished:
        await message.reply(f"Ваша вага: {weight} кг\nМета: {water_meta_amount} мл\nВипито води за сьогодні: {today_water} мл\n🎉 Вітаємо! Ви випили достатню кількість води сьогодні!", reply_markup=MetaKeyboard().get_keyboard())
    else:
        await message.reply(f"Ваша вага: {weight} кг\nМета: {water_meta_amount} мл\nВипито води за сьогодні: {today_water} мл\nДо мети залишилось {water_meta_amount - today_water} мл", reply_markup=MetaKeyboard().get_keyboard())



@dp.message_handler(state=MetaStates.WEIGHT)
async def meta_weight(message: types.Message):
    user_id = message.from_user.id
    weight = message.text
    state = dp.current_state(user=user_id)

    if weight.isdigit():
        try:
            weight = float(weight)
            # Збереження ваги користувача
            query = "UPDATE user SET weight = %s, water_meta_amount = %s WHERE user_id = %s"
            water_meta_amount = weight * 30
            execute_query(query, weight, water_meta_amount, user_id)
            await message.reply("Вагу збережено", reply_markup=StartKeyboard(user_id).get_keyboard())
            await state.reset_state()
        except ValueError:
            await message.reply("Некоректне значення. Будь ласка, введіть вашу вагу у кг:")
    else:
        await message.reply("Некоректне значення. Будь ласка, введіть вашу вагу у кг:")



daily_water_reminder = DailyWaterReminder()


async def start_schedule():
    await daily_water_reminder.schedule_water_reminder()

# Start the bot
async def start_bot():
    await bot.set_my_commands([types.BotCommand("start", "Запустити бота")])
    await dp.start_polling()

# Run the bot and schedule concurrently
async def main():

     await asyncio.gather(start_schedule(), start_bot())


if __name__ == '__main__':
    try:
        create_tables()
        asyncio.run(main())
    finally:
        # Close the database connection on exit
        cursor.close()
        db.close()