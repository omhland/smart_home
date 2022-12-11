from todoist_api_python.api import Task, Section, Label, Collaborator
from datetime import datetime

"""
This script defines all filters that we want to use on task data.

Each filter assumes a list of tasks as input and returns a filtered list of tasks as output.
"""

# Convenience functions
def get_task_datetime(task:Task):
    date_string = task.due.date
    return datetime.strptime(date_string, '%Y-%m-%d')

def has_due_date(task:Task):
    return task.due is not None

def has_assignee(task:Task):
    return task.assignee_id is not None

def in_section(task:Task, section_id:str):
    return task.section_id == section_id

# Various filters

def tasks_with_due_date(tasks:list):
    return [task for task in tasks if has_due_date(task)]

def tasks_with_assignee(tasks:list):
    return [task for task in tasks if has_assignee(task)]

def uncompleted_tasks(tasks:list):
    return [task for task in tasks if not task.is_completed]

def active_assigned_tasks(tasks:list):
    tasks = uncompleted_tasks(tasks)
    tasks = tasks_with_assignee(tasks)
    return tasks

def tasks_due_within_days(tasks:list, days:int):
    tasks = uncompleted_tasks(tasks)
    tasks = tasks_with_due_date(tasks)
    return [task for task in tasks if (get_task_datetime(task) - datetime.now()).days <= days]

def tasks_in_section(tasks:list, section:Section):
    return [task for task in tasks if in_section(task, section.id)]
