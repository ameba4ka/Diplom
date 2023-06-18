from datetime import datetime, timedelta
from . import utils 
# Коефіцієнти для різних типів рідин
liquid_coefficients = {
    "water": 1.0,
    "juice": 0.8,
    "alcohol": 0.4,
    "sparkling_water": 0.9,
    "coffee": 0.5,
    "tea": 0.6,
    "milk": 0.7
}

# Функція для вставки нового запису про вживання рідини
def insert_liquid_intake(user_id, liquid_type, amount):
    coefficient = liquid_coefficients.get(liquid_type, 1.0)  # Отримати коефіцієнт для заданого типу рідини
    adjusted_amount = round(amount * coefficient,2)  # Враховувати коефіцієнт при розрахунку кількості рідини
    query = "INSERT INTO LiquidIntake (user_id, consumed_date, liquid_type, amount) VALUES (%s, %s, %s, %s)"
    now = datetime.now()
    utils.execute_query(query, user_id, now, liquid_type, adjusted_amount)