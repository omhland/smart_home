from todoist_data_collector import Project, TASK_MAP, print_map
# Create any kind of filter function you want and import it here
from filters import tasks_in_section, uncompleted_tasks, tasks_due_within_days

# Specify the project to use
project_name = 'Kool Kids'
# Specify the section of interest
section_name = 'chores'

project = Project(project_name)
chore_section = project.get_section_by_name(section_name)

filters = [
    (tasks_in_section, {'section': chore_section}),
    (tasks_due_within_days, {'days': 1}),
    (uncompleted_tasks, {}),
]

collaborator_task_map = project.filter_map(TASK_MAP.COLLABORATOR, filters)

print_map(collaborator_task_map, project, TASK_MAP.COLLABORATOR)
