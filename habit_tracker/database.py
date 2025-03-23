import sqlite3
from sqlite3 import Error
import os
from .habit import Habit

""" 
Database class including the SQLite persistence system for keeping habit records.
"""

class Database:
    def __init__(self):
        """
        Initializes database connection and creates tables.
        """
        self.db_path = "data/habits.db"
        os.makedirs("data", exist_ok=True)
        self.create_tables()

    def create_tables(self):
        """
        Creates habits and completions tables.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        periodicity TEXT NOT NULL,
                        category TEXT,
                        creation_date TEXT NOT NULL
                    )
                ''')
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS completions (
                        completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id INTEGER NOT NULL,
                        completion_date TEXT NOT NULL,
                        FOREIGN KEY(id) REFERENCES habits(id)
                    )
                ''')
        except Error as e:
            print(f"Database error: {e}")

    def save_habit(self, habit: Habit):
        """
        Saves habit and its completions to the database.
        :param habit: Habit to save.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if habit.id is None:
                    cursor.execute('SELECT id FROM habits WHERE name = ?', (habit.name,))
                    existing_habit = cursor.fetchone()
                    if existing_habit:
                        raise ValueError(f"Habit with name '{habit.name}' already exists.")
                    cursor.execute('''
                        INSERT INTO habits (name, periodicity, category, creation_date)
                        VALUES (?, ?, ?, ?)
                    ''', (habit.name, habit.periodicity, habit.category, habit.creation_date))
                    habit.id = cursor.lastrowid
                else:
                    cursor.execute('''
                    UPDATE habits
                    SET name=?, periodicity=?, category=?, creation_date=?
                    WHERE id=?
                    ''',(habit.name, habit.periodicity, habit.category, habit.creation_date, habit.id))
                cursor.execute('DELETE FROM completions WHERE id=?', (habit.id,))
                for date in habit.completion_dates:
                    cursor.execute('''
                    INSERT INTO completions (id, completion_date)
                    VALUES (?,?)
                    ''', (habit.id, date))
                conn.commit()
        except Error as e:
            print(f"Error saving habit: {e}")

    def delete_habit(self, id: int):
        """
        Deletes habit and its completions from the database.
        :param id: Habit ID to delete.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM habits WHERE id = ?', (id,))
                cursor.execute('DELETE FROM completions WHERE id = ?', (id,))
                conn.commit()
        except Error as e:
            print(f"Error deleting habit: {e}")

    def load_habits(self) -> list[Habit]:
        """
        Loads habits and completions from the database.
        """
        habits = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM habits')
                for row in cursor.fetchall():
                    habit = Habit(row[1], row[2], row[3])
                    habit.id, habit.creation_date = row[0], row[4]
                    cursor.execute('''
                        SELECT completion_date 
                        FROM completions 
                        WHERE id = ?''',
                        (habit.id,))
                    habit.completion_dates = [row[0] for row in cursor.fetchall()]
                    habits.append(habit)
        except Error as e:
            print(f"Error loading habits: {e}")
        return habits