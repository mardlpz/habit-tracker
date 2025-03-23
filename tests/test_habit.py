import pytest
from habit_tracker.habit import Habit
from datetime import datetime, timedelta
from habit_tracker.analytics import *

""" 
Testing module including a unit test suite for validating core functionality of the application.
"""

@pytest.fixture
def sample_daily_habit():
    """
    Fixture for a daily habit with example completion data for 28 days.
    """
    habit = Habit("Exercise", "daily", "health")
    habit.creation_date = (datetime.now() - timedelta(days=27)).isoformat()
    habit.completion_dates = [
        (datetime.now() - timedelta(days=i)).isoformat() for i in range(3)
    ]
    return habit

@pytest.fixture
def sample_weekly_habit():
    """
    Fixture for a weekly habit with example completion data for 4 weeks.
    """
    habit = Habit("Yoga", "weekly", "health")
    habit.creation_date = (datetime.now() - timedelta(weeks=3)).isoformat()
    habit.completion_dates = [
        (datetime.now() - timedelta(weeks=i)).isoformat() for i in range(4)
    ]
    return habit

def test_longest_streak_daily(sample_daily_habit: Habit):
    """
    Test the longest streak calculation for a daily habit.
    :param sample_daily_habit: Fixture for a daily habit.
    """
    assert calculate_longest_streak_habit(sample_daily_habit) == 3

def test_longest_streak_weekly(sample_weekly_habit: Habit):
    """
    Test the longest streak calculation for a weekly habit.
    :param sample_weekly_habit: Fixture for a weekly habit.
    """
    assert calculate_longest_streak_habit(sample_weekly_habit) == 4

def test_current_streak_daily(sample_daily_habit: Habit):
    """
    Test the current streak calculation for a daily habit.
    :param sample_daily_habit: Fixture for a daily habit.
    """
    assert calculate_current_streak(sample_daily_habit) == 3

def test_current_streak_weekly(sample_weekly_habit: Habit):
    """
    Test the current streak calculation for a weekly habit.
    :param sample_weekly_habit: Fixture for a weekly habit.
    """
    assert calculate_current_streak(sample_weekly_habit) == 4

def test_completion_rate_daily(sample_daily_habit: Habit):
    """
    Test the completion rate calculation for a daily habit.
    :param sample_daily_habit: Fixture for a daily habit.
    """
    assert get_completion_rate(sample_daily_habit) == 3.0 / 28.0

def test_completion_rate_weekly(sample_weekly_habit: Habit):
    """
    Test the completion rate calculation for a weekly habit.
    :param sample_weekly_habit: Fixture for a weekly habit.
    """
    assert get_completion_rate(sample_weekly_habit) == 4.0 / 4.0

def test_average_completion_rate(sample_daily_habit: Habit, sample_weekly_habit: Habit):
    """
    Test the average completion rate calculation across all habits.
    :param sample_daily_habit: Fixture for a daily habit.
    :param sample_weekly_habit: Fixture for a weekly habit.
    """
    habits = [sample_daily_habit, sample_weekly_habit]
    total_completion_rate = sum(get_completion_rate(habit) for habit in habits)
    average = total_completion_rate / len(habits)
    assert average == ((3.0 / 28.0) + (4.0 / 4.0)) / 2

def test_weekly_report(sample_daily_habit: Habit, sample_weekly_habit: Habit):
    """
    Test the weekly report generation.
    :param sample_daily_habit: Fixture for a daily habit.
    :param sample_weekly_habit: Fixture for a weekly habit.
    """
    habits = [sample_daily_habit, sample_weekly_habit]
    report = generate_weekly_report(habits)
    assert report[sample_daily_habit.name] == True
    assert report[sample_weekly_habit.name] == True

def test_monthly_report(sample_daily_habit: Habit, sample_weekly_habit: Habit):
    """
    Test the monthly report generation.
    :param sample_daily_habit: Fixture for a daily habit.
    :param sample_weekly_habit: Fixture for a weekly habit.
    """
    habits = [sample_daily_habit, sample_weekly_habit]
    report = generate_monthly_report(habits)
    assert report[sample_daily_habit.name] == True
    assert report[sample_weekly_habit.name] == True
