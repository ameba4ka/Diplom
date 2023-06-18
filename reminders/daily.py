import aioschedule as schedule
import asyncio
from datetime import datetime
from loader import bot
from db import cursor

class DailyWaterReminder():
    def __init__(self):
        self.interval_minutes = 60
        self.reminder_message = "Час пити воду! 💧"
        self.user_chat_ids = []

    # Get all the user chat ids from db
    def get_user_chat_ids(self):
        query = """
            SELECT user_id
            FROM user;
            """

        cursor.execute(query)

        for user in cursor.fetchall():
            self.user_chat_ids.append(user['user_id'])
    

    # def calculate_optimized_interval(self, user_id):
    #     query = """
    #         SELECT *
    #         FROM liquidIntake
    #         JOIN user ON liquidIntake.user_id = user.user_id
    #         WHERE user.user_id = %s
    #         ORDER BY liquidIntake.consumed_date DESC
    #         LIMIT 1;
    #         """
    #     user = execute_query(query, user_id)[0]
    #     previous_time = user['consumed_date']
    #     print("previous_time:", previous_time)
    #     if previous_time:
    #         time_since_previous = datetime.now() - previous_time
    #         minutes_since_previous = time_since_previous.total_seconds() / 60
    #         print("minutes_since_previous:", minutes_since_previous)
    #         optimized_interval = max(60, minutes_since_previous)  # Minimum interval of 60 minutes
    #         return int(optimized_interval)
    #     else:
    #         return 60  # Default interval of 60 minutes if no previous consumption time is available



    async def send_water_reminder_by_user(self, user_id):
        current_hour = datetime.now().hour
        try:
            if current_hour >= 6 and current_hour < 23: # 6am to 11pm
                await bot.send_message(user_id, self.reminder_message)
        except Exception as e:
            print(e)

    # Schedule the water reminder task with optimized interval
    async def schedule_water_reminder(self):
        # Get all the user chat ids from db
        self.get_user_chat_ids()
        # Schedule the water reminder task for every sindle user
        print(self.user_chat_ids)
        for user_id in self.user_chat_ids:
            schedule.every(self.interval_minutes).minutes.do(self.send_water_reminder_by_user, user_id)
        # Run the scheduler
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)

    def update_reminder(self, user_id):
        schedule.clear(user_id)
        schedule.every(self.interval_minutes).minutes.do(self.send_water_reminder_by_user, user_id)