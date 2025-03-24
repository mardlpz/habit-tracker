import os
import sys
import click
from tabulate import tabulate
from habit_tracker.database import Database
from habit_tracker.habit import Habit
from habit_tracker.analytics import *

"""
Command-line interface module including all the commands available to the user when running the application on terminal.
"""

@click.group()
def cli():
    """
    Habit tracker command line interface.
    """
    pass

@cli.command()
@click.option("--task", "--t", required=True, type=str, help="Task name (e.g. 'exercise')")
@click.option("--periodicity", "--p", required=True, type=click.Choice(["daily", "weekly"]), help="Periodicity ('daily' or 'weekly')")
@click.option("--category", "--c", default="general", type=str, help="Category (e.g. 'health')")
def create(task: str, periodicity: str, category: str):
    """
    Create a habit and save it to database.
    :param task: Task name (e.g. 'exercise')
    :param periodicity: Periodicity ('daily' or 'weekly')
    :param category: Category (e.g. 'general')
    """
    try:
        habit = Habit(task, periodicity, category)
        db = Database()
        db.save_habit(habit)
        click.echo(f"Created {periodicity} {category} habit: {task} (ID: {habit.id})")
    except ValueError as e:
        click.echo(f"Error:  {str(e)}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option("--id", type=int, required=True, help="Habit ID to complete")
def complete(id: int):
    """
    Mark habit as complete.
    :param id: Habit ID to complete.
    """
    try:
        db = Database()
        habits = db.load_habits()
        habit = next((habit for habit in habits if habit.id == id), None)
        if not habit:
            raise ValueError(f"No habit with ID {id} found.")
        habit.complete_habit()
        db.save_habit(habit)
        click.echo(f"Completed habit: {habit.name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option("--periodicity", "--p", type=click.Choice(["daily", "weekly"]), help="Filter habits by periodicity ('daily' or 'weekly')")
@click.option("--category", "--c", type=str, help="Filter habits by category (e.g. 'health')")
def list(periodicity: str, category: str):
    """
    List all habits, filter by periodicity or category if desired.
    :param periodicity: Periodicity to filter by ('daily' or 'weekly')
    :param category: Category to filter by (e.g. 'general')
    """
    try:
        db = Database()
        habits = db.load_habits()
        if periodicity:
            habits = get_by_periodicity(habits, periodicity)
        if category:
            habits = get_by_category(habits, category)

        table = [[habit.id, habit.name, habit.periodicity, habit.category] for habit in habits]
        click.echo(tabulate(table, headers=["ID", "Task", "Periodicity", "Category"]))
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option("--id", type=int, help="Habit ID to analyze.")
@click.option("--periodicity", "--p", type=click.Choice(["daily", "weekly"]), help="Filter habits by periodicity ('daily' or 'weekly')")
@click.option("--category", "--c", type=str, help="Filter habits by category (e.g. 'health')")
@click.option("--longest-streak", "--ls", is_flag=True, help="Calculate the longest streak.")
@click.option("--current-streak", "--cs", is_flag=True, help="Calculate the current streak.")
@click.option("--completion-rate", "--cr", is_flag=True, help="Calculate completion rate.")
@click.option("--most-struggled", "--ms", is_flag=True, help="Calculate habit struggled with the most.")
@click.option("--weekly-report", "--wr", is_flag=True, help="Calculate weekly report for habits.")
@click.option("--monthly-report", "--mr", is_flag=True, help="Calculate monthly report for habits.")
def analyze(id: int, periodicity: str, category: str, longest_streak, current_streak, completion_rate, most_struggled, weekly_report, monthly_report):
    """
    Analyze all habits, or a specific habit by ID.
    :param id: Habit ID to analyze.
    :param periodicity: Periodicity to filter by ('daily' or 'weekly')
    :param category: Category to filter by (e.g. 'health')
    :param longest_streak: Option to calculate the longest streak.
    :param current_streak: Option to calculate the current streak.
    :param completion_rate: Option to calculate completion rate.
    :param most_struggled: Option to calculate the most struggled.
    :param weekly_report: Option to calculate weekly report.
    :param monthly_report: Option to calculate monthly report.
    """
    try:
        db = Database()
        habits = db.load_habits()
        if periodicity:
            habits = get_by_periodicity(habits, periodicity)
        if category:
            habits = get_by_category(habits, category)
        if id:
            habit = next((habit for habit in habits if habit.id == id), None)
            if not habit:
                raise ValueError(f"No habit with ID {id} found.")
            if longest_streak:
                click.echo(f"Longest streak for {habit.name}: {calculate_longest_streak_habit(habit)}")
            if current_streak:
                click.echo(f"Current streak for {habit.name}: {calculate_current_streak(habit)}")
            if completion_rate:
                click.echo(f"Completion rate for {habit.name}: {get_completion_rate(habit) * 100:.2f}%")
            if most_struggled:
                click.echo(f"Feature not available for a single habit ID.")
            if weekly_report:
                click.echo(f"Feature not available for a single habit ID.")
            if monthly_report:
                click.echo(f"Feature not available for a single habit ID.")
        else:
            if longest_streak:
                click.echo(f"Longest streak across all habits: {calculate_longest_streak_all(habits)}")
            if current_streak:
                click.echo("Current streaks:")
                for h in habits:
                    click.echo(f"- {h.name}: {calculate_current_streak(h)}")
            if completion_rate:
                total_completion_rate = sum(get_completion_rate(habit) for habit in habits)
                average = total_completion_rate / len(habits) if habits else 0
                click.echo(f"Average completion rate across all habits: {average * 100:.2f}%")
            if most_struggled:
                struggled = get_most_struggled_habit(habits)
                click.echo(f"Most struggled habit: {struggled.name if struggled else 'None'}")
            if weekly_report:
                report = generate_weekly_report(habits)
                click.echo("\nWeekly Report:")
                for name, completed in report.items():
                    click.echo(f"- {name}: {'Completed' if completed else 'Not completed'}")
            if monthly_report:
                report = generate_monthly_report(habits)
                click.echo("\nMonthly Report:")
                for name, completed in report.items():
                    click.echo(f"- {name}: {'Completed' if completed else 'Not completed'}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
@click.option("--id", type=int, required=True, help="Habit ID to delete.")
def delete(id: int):
    """
    Delete habit by ID.
    :param id: Habit ID to delete.
    """
    try:
        db = Database()
        db.delete_habit(id)
        click.echo(f"Deleted habit with ID: {id}")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def reset():
    """
    Reset database file.
    """
    try:
        db = Database()
        if os.path.exists("data/habits.db"):
            os.remove("data/habits.db")
            click.echo(f"Database reset successfully.")
        else:
            click.echo("Database file does not exist.")
        db.create_tables()
        click.echo("Database reinitialized.")
    except Exception as e:
        click.echo(f"Error: {str(e)}")

@cli.command()
def exit():
    """
    Exit the program and clear terminal screen.
    """
    try:
        click.echo("Exiting program.")
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit(0)
    except Exception as e:
        click.echo(f"Error: {str(e)}")

if __name__ == "__main__":
    cli()



