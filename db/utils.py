from db import db

# Функція для виконання запиту до бази даних
def execute_query(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    db.commit()
    return result