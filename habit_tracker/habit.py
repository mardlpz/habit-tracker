from datetime import datetime

"""
Habit class including constructor for individual habits with all attributes and completion.
"""


class Habit:
    """
    Represents individual habits.
    """
    def __init__(self, name: str, periodicity: str, category: str):
        """
        Initializes habit with task name, periodicity, and category.
        :param name: Name of the habit (e.g., "Exercise").
        :param periodicity: Frequency of the habit ("daily" or "weekly").
        :param category: Category of the habit (e.g., "health").
        """
        self.id = None
        self.name = name
        self.periodicity = periodicity
        self.category = category
        self.creation_date = datetime.now().isoformat()
        self.completion_dates = []

    def complete_habit(self):
        """
        Records habit completion timestamp.
        """
        self.completion_dates.append(datetime.now().isoformat())


