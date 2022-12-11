from todoist_data_collector import Project, TASK_MAP, print_map
from filters import tasks_in_section, uncompleted_tasks, tasks_due_within_days

project_name = 'Kool Kids'
section_name = 'chores'

project = Project(project_name)

chore_section = project.get_section_by_name(section_name)

filters = [
    (tasks_due_within_days, {'days': 1}),
    (uncompleted_tasks, {}),
    (tasks_in_section, {'section': chore_section}),
]

filtered_map = project.filter_map(TASK_MAP.COLLABORATOR, filters)

print_map(filtered_map, project, TASK_MAP.COLLABORATOR)
