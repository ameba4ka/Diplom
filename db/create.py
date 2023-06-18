from . import utils

# Створення таблиць у базі даних
def create_tables():
    query = """
    CREATE TABLE IF NOT EXISTS User (
        user_id INT PRIMARY KEY,
        username VARCHAR(255),
        water_amount FLOAT DEFAULT 0,
        juice_amount FLOAT DEFAULT 0,
        alcohol_amount FLOAT DEFAULT 0,
        sparkling_water_amount FLOAT DEFAULT 0,
        coffee_amount FLOAT DEFAULT 0,
        tea_amount FLOAT DEFAULT 0,
        milk_amount FLOAT DEFAULT 0
    )
    """
    utils.execute_query(query)

    query = """
    CREATE TABLE IF NOT EXISTS LiquidIntake (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT,
        consumed_date DATETIME,
        liquid_type VARCHAR(255),
        amount FLOAT,
        weight FLOAT,
        water_meta_amount FLOAT,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
    """
    utils.execute_query(query)