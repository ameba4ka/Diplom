from . import utils

# Функція для вставки нового користувача в таблицю User
def insert_user(user_id, username):
    query = "INSERT INTO User (user_id, username) VALUES (%s, %s)"
    utils.execute_query(query, user_id, username)

# Функція для отримання статистики за певний період
def get_statistics(user_id, start_date, end_date, today = False):
    today_query = """
    SELECT liquid_type, SUM(amount)
    FROM LiquidIntake
    WHERE user_id = %s AND consumed_date >= %s AND consumed_date < %s
    GROUP BY liquid_type
    """
    week_query = """
    SELECT liquid_type, SUM(amount)
    FROM LiquidIntake
    WHERE user_id = %s AND consumed_date >= %s AND consumed_date <= %s
    GROUP BY liquid_type
    """

    result = utils.execute_query(today_query if today else week_query, user_id, 
    start_date.replace(hour=0, minute=0, second=0, microsecond=0), 
    end_date.replace(hour=23, minute=59, second=59, microsecond=9999))
    return result