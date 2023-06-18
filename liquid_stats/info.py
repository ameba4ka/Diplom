from datetime import datetime, timedelta
from db.user import get_statistics
import logging
from message import KEYBOARD_TEXT

# Функція для отримання дати, зменшеної на певну кількість днів
def get_past_date(days):
    today = datetime.now()
    past_date = today - timedelta(days=days)
    return past_date


# Функція для форматування статистики у текстовий рядок
def format_statistics(statistics):
    total_amount = 0
    message = "Статистика вжитої рідини:\n"
    for row in statistics:
        liquid_type, amount = row.values()
        total_amount += amount
        message += f"{KEYBOARD_TEXT.get(liquid_type)}: {round(amount,2)} мл\n"
    message = f"Загальна кількість рідини: {round(total_amount,2)} мл\n\n" + message
    return {"message": message, "total_amount": total_amount}

# Функція для обробки команди /stats
def get_formated_statistics(user_id):

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Отримання статистики за сьогодні
    # today = datetime.fromisoformat(datetime.now().date().isoformat())
    today_statistics = get_statistics(user_id, today, today, True)

    # # Отримання статистики за вчора
    # yesterday = get_past_date(1)
    yesterday_statistics = get_statistics(user_id, yesterday, yesterday, True)

    # # Отримання статистики за тиждень
    # week_start = get_past_date(7)
    week_statistics = get_statistics(user_id, start_of_week, today)

    # # Отримання статистики за місяць
    # month_start = get_past_date(30)
    month_statistics = get_statistics(user_id, start_of_month, today)

    # Форматування статистики у текстові рядки
    today_message = format_statistics(today_statistics)['message']
    yesterday_message = format_statistics(yesterday_statistics)['message']
    week_message = format_statistics(week_statistics)['message']
    month_message = format_statistics(month_statistics)['message']

    # Створення повідомлення зі статистикою
    message = "Статистика рідини:\n\n"
    message += f"Сьогодні:\n{today_message}\n"
    message += f"Вчора:\n{yesterday_message}\n"
    message += f"Тиждень:\n{week_message}\n"
    message += f"Місяць:\n{month_message}\n"

    # Відправка повідомлення зі статистикою
    return message

def today_statistics(user_id):
    today = datetime.now()
    today_statistics = get_statistics(user_id, today, today, True)
    return format_statistics(today_statistics)['total_amount']
