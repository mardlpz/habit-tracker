from datetime import datetime, timedelta
from typing import List
from .habit import Habit

""" 
Analytics module including all the functions to analyze habit information and records.
"""


def get_all(habits: List[Habit]) -> List[Habit]:
    """
    Return all habits.
    :param habits: List of habits.
    """
    return habits

def get_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    Filter habits by periodicity.
    :param habits: List of habits.
    :param periodicity: Periodicity to filter (e.g., "health").
    """
    return [habit for habit in habits if habit.periodicity == periodicity]

def get_by_category(habits: List[Habit], category: str) -> List[Habit]:
    """
    Filter habits by category.
    :param habits: List of habits.
    :param category: Category to filter by ("weekly" or "daily").
    :return:
    """
    return [habit for habit in habits if habit.category == category]

def calculate_longest_streak_all(habits: List[Habit]) -> int:
    """
    Calculate longest streak across all habits.
    :param habits: List of habits.
    """
    return max((calculate_longest_streak_habit(habit) for habit in habits), default = 0)

def calculate_longest_streak_habit(habit: Habit) -> int:
    """
    Calculate longest streak for a specific habit.
    :param habit: Habit to calculate longest streak for.
    """
    if not habit.completion_dates:
        return 0
    dates = sorted([datetime.fromisoformat(date) for date in habit.completion_dates])
    streak = max_streak = 1
    for i in range(1, len(dates)):
        delta = (dates[i].date() - dates[i - 1].date()).days if habit.periodicity == "daily" else (dates[i].isocalendar()[1] - dates[i - 1].isocalendar()[1])
        streak = streak + 1 if delta == 1 else 1
        max_streak = max(streak, max_streak)
    return max_streak

def calculate_current_streak(habit: Habit) -> int:
    """
    Calculate current streak for a specific habit.
    :param habit: Habit to calculate current streak for.
    """
    if not habit.completion_dates:
        return 0
    dates = sorted([datetime.fromisoformat(date).date() for date in habit.completion_dates], reverse=True)
    today = datetime.now().date()
    delta = timedelta(days=1) if habit.periodicity == "daily" else timedelta(weeks=1)
    streak = 0
    for i, date in enumerate(dates):
        if i == 0:
            if (today - date) > delta:
                break
            streak += 1
        else:
            if (dates[i - 1] - date) == delta:
                streak += 1
            else:
                break
    return streak

def get_most_struggled_habit(habits: List[Habit]) -> Habit:
    """
    Get habit with most broken streaks
    :param habits: List of habits.
    """
    def count_missed_periods(habit: Habit):
        missed = 0
        dates = sorted([datetime.fromisoformat(date).date() for date in habit.completion_dates])
        for i in range(1, len(dates)):
            previous, current = dates[i-1], dates[i]
            expected = previous + timedelta(days=1) if habit.periodicity == "daily" else previous + timedelta(weeks=1)
            if current > expected:
                missed += 1
        return missed
    return max(habits, key=lambda habit: count_missed_periods(habit), default=None) if habits else None

def get_completion_rate(habit: Habit) -> float:
    """
    Calculate completion rate for a habit.
    :param habit: Habit to calculate completion rate for.
    """
    if not habit.completion_dates:
        return 0.0
    creation_date = datetime.fromisoformat(habit.creation_date).date()
    today = datetime.now().date()
    if habit.periodicity == "daily":
        total_periods = (today - creation_date).days + 1
    else:
        creation_week = creation_date.isocalendar()[1]
        current_week = today.isocalendar()[1]
        total_periods = (current_week - creation_week) + 1

    if total_periods <= 0:
        return 0.0
    return len(habit.completion_dates) / total_periods

def generate_weekly_report(habits: List[Habit]) -> dict:
    """
    Generate weekly report for all habits.
    :param habits: List of habits.
    """
    report = dict()
    today = datetime.now().date()
    week = today.isocalendar()[1]

    for habit in habits:
        completed = any(datetime.fromisoformat(date).isocalendar()[1] == week for date in habit.completion_dates)
        report[habit.name] = completed
    return report

def generate_monthly_report(habits: List[Habit]) -> dict:
    """
    Generate monthly report for all habits.
    :param habits: List of habits.
    """
    report = dict()
    today = datetime.now().date()
    month = today.month
    for habit in habits:
        completed = any(datetime.fromisoformat(date).month == month for date in habit.completion_dates)
        report[habit.name] = completed
    return report
