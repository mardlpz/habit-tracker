# HABIT TRACKING APP

A python-powered command-line application for tracking and analyzing daily/weekly habits. Built with object-oriented and functional programming paradigms.


## Features
1. **Create Habits**: Define habits by task name, periodicity, and category.
2. **Track Completion**: Record timestamps for habit completions.
3. **Analyze Progress**: Calculate streaks, filter habits by periodicity/category, and generate reports.
4. **Data Management**: Habits stored locally in an SQLite database.
4. **Command-line UI**: User-friendly interface with `click`.


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mardlpz/habit-tracker.git  
   ```

2. **Navigate to project directory:**

   (Replace with actual local path to cloned repository.)
   ```bash
   cd path/to/habit-tracker
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv .venv
   ```
   
4. **Activate virtual environment**:
   
   On macOS/Linux:
   ```bash
   source .venv/bin/activate 
    ```
   On Windows:
    ```bash
   .venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
<br/>

## Usage

- **Basic command-line interaction:**
   
      python -m habit_tracker.cli <command> --[option]
<br/>

1. **Create habits**
   - Command: `create`
   - Options:
     - Task name (mandatory, string): `--task` or `--t`
     - Periodicity (mandatory, 'daily' or 'weekly'): `--periodicity` or `--p`
     - Category (optional, default: general): `--category` or `--c`
   - Example:
   ```bash
   python -m habit_tracker.cli create --task "Exercise" --periodicity daily --category health
   ```

2. **Complete a Habit**
   - Command: `complete`
   - Options:
     - ID (mandatory): `--id`
   - Example:
   ```bash
   python -m habit_tracker.cli complete --id 4
   ```

3. **List Habits**
   - Command: `list`
   - Options (default: lists all habits):
     - Periodicity (optional, 'daily' or 'weekly'): `--periodicity` or `--p`
     - Category (optional): `--category` or `--c`
   - Example:
   ```bash
   python -m habit_tracker.cli list --periodicity weekly --category education
   ```

4. **Analyze Habits**
      - Command: `analyze`
      - Options:
        - ID (for specific habit analysis): `--id`
        - Periodicity: `--periodicity` or `--p`
        - Category: `--category` or `--c`
        - Longest streak: `--longest-streak` or `--ls`
        - Current streak: `--current-streak` or `--cs`
        - Completion rate: `--completion-rate` or `--cr`
        - Most struggled habit: `--most-struggled` or `--ms`
        - Weekly report: `--weekly-report` or `--wr`
        - Monthly report: `--monthly-report` or `--mr`
      - Example:
      ```bash
      python -m habit_tracker.cli analyze --longest-streak
      python -m habit_tracker.cli analyze --current-streak
      python -m habit_tracker.cli analyze --completion-rate
      python -m habit_tracker.cli analyze --most-struggled
      python -m habit_tracker.cli analyze --weekly-report
      python -m habit_tracker.cli analyze --monthly-report
      ```
   
*`--most-struggled`, `--weekly-report`, and `--monthly-report` do not apply for specific analysis by ID, cannot be performed on a single habit.

5. **Delete a Habit**
   - Command: `delete`
   - Options:
     - ID (mandatory): `--id`
   - Example:
   ```bash
   python -m habit_tracker.cli delete --id 4
   ```

6. **Reset database**
   - Command: `reset`
   - Example:
   ```bash
   python -m habit_tracker.cli reset
   ```

7. **Exit and clear terminal**
   - Command: `exit`
   - Example:
   ```bash
   python -m habit_tracker.cli exit
   ```
<br/>

## Persistence

Habit data is stored in an SQLite database contained within the file 
"habits.db" (data/habits.db). The database is automatically created if it doesn’t exist yet.
When opening the file in an IDE such as PyCharm, habits and completions tables can be visualized
in ascending and descending order. It is important to refresh the file after an operation has
been performed on the database.
<br/>

## Sample Data

The application provides a file with sample data (`sample_data.py`) including 5 predefined habits with 4 weeks of tracking records each:

- Drink Water (Daily, Health)
- Yoga (Weekly, Health)
- Read (Daily, Education)
- Journal (Weekly, Mental Health)
- Meditate (Daily, Mental Health)  

Load sample data into database with:
   ```bash
   python sample_data.py
   ```
<br/>
   
## Testing

The application includes a collection of pytest test cases to validate the core functionality. The test fixtures 
provide sample habit data with predefined completion dates to ensure consistent and reproducible test results.
Run the unit tests with:
   ```bash
   pytest tests/
   ```
<br/>

## Deactivate virtual environment 
Exit and deactivate the virtual environment with:
   ```bash
   deactivate
   ```
<br/>

## Help & Documentation 

All code is documented with descriptive Python docstrings for further clarification.
To access the help documentation directly from the command-line interface use the following commands:
- General help:
   ```bash
   python -m habit_tracker.cli --help
   ```
- Command-specific help:
   ```bash
   python -m habit_tracker.cli analyze --help
   python -m habit_tracker.cli complete --help
   python -m habit_tracker.cli create --help
   python -m habit_tracker.cli delete --help
   python -m habit_tracker.cli exit --help
   python -m habit_tracker.cli list --help
   python -m habit_tracker.cli reset --help
   ```
<br/>
 
## Information
Author: Mariana Del Pozo Patrón  
Python version: 3.12.3  
Publish date: March 23, 2025  
Object Oriented and Functional Programming with Python  
International University of Applied Sciences  

