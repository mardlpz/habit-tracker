from datetime import datetime, timedelta
from habit_tracker.database import Database
from habit_tracker.habit import Habit

"""
Sample data file including load function for the predefined habits and tracking records.
"""

def load_sample_data():
    """
    Loads 5 predefined habits with example tracking data for 4 weeks.
    """
    habits = [
        Habit("Drink Water", "daily", "health"),
        Habit("Yoga", "weekly", "health"),
        Habit("Read", "daily", "education"),
        Habit("Journal", "weekly", "mental health"),
        Habit("Meditate", "daily", "mental health")
    ]

    today = datetime.now().date()
    for habit in habits:
        if habit.periodicity == "daily":
            habit.creation_date = (today - timedelta(days=27)).isoformat()
            for i in range(28):
                completion_date = today - timedelta(days=i)
                habit.completion_dates.append(completion_date.isoformat())
        else:
            habit.creation_date = (today - timedelta(weeks=3)).isoformat()
            for i in range(4):
                completion_date = today - timedelta(weeks=i)
                habit.completion_dates.append(completion_date.isoformat())

    db = Database()
    for habit in habits:
        db.save_habit(habit)

    print("Loaded 5 predefined habits with sample tracking data for 4 weeks.")

if __name__ == "__main__":
    load_sample_data()