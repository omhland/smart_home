from todoist_api_python.api import TodoistAPI, Task, Section, Label, Collaborator
from pathlib import Path
from typeguard import typechecked

from enum import Enum, auto
from dataclasses import dataclass

token_file = '.token'
# Verify that the token file exists
if not Path(token_file).is_file():
    print('Token file not found')
    exit()
else:
    with open(token_file, 'r') as f:
        token = f.read().strip()

class todoist_client:
    api = TodoistAPI(token)
    tasks = api.get_tasks()
    projects = api.get_projects()
    sections = api.get_sections()

    @classmethod
    def get_project_names(cls):
        return [project.name for project in cls.projects]

    @classmethod
    @typechecked
    def get_project_from_name(cls, name:str):
        for project in cls.projects:
            if project.name == name:
                return project

    @classmethod
    @typechecked
    def get_project_tasks(cls, project_name:str):
        project = cls.get_project_from_name(project_name)
        project_id = project.id
        project_tasks = []

        for task in cls.tasks:
            if task.project_id == project_id:
                project_tasks.append(task)

        return project_tasks

    @classmethod
    @typechecked
    def get_section_tasks(cls, section_id:str):
        section_tasks = []
        for task in cls.tasks:
            if task.section_id == section_id:
                section_tasks.append(task)

        return section_tasks

    @classmethod
    @typechecked
    def get_section_task_ids(self, section_id:str):
        section_tasks = self.get_section_tasks(section_id)
        task_ids = [task.id for task in section_tasks]
        return task_ids

    @classmethod
    @typechecked
    def get_project_sections(cls, project_name:str):
        project = cls.get_project_from_name(project_name)
        project_id = project.id
        project_sections = []

        for section in cls.sections:
            if section.project_id == project_id:
                project_sections.append(section)

        return project_sections

    @classmethod
    def get_section_name_tasks(cls, section_name:str, project_name:str=None):
        """
        Returns a list of tasks for a given section name

        Args:
            section_name (str): The name of the section to search for
            project_name (str, optional): Restrict the search to a specific project. Defaults to None.

        Returns:
            list: A list of tasks
        """
        section_id = None
        for section in cls.sections:
            if section.name == section_name:
                section_id = section.id
                break

        if section_id is None:
            raise Exception(f'Section {section_name} not found')

        section_tasks = []

        if project_name is not None:
            project = cls.get_project_from_name(project_name)
            condition = lambda task: task.section_id == section_id and task.project_id == project.id
        else:
            condition = lambda task: task.section_id == section_id

        for task in cls.tasks:
            if condition(task):
                section_tasks.append(task)

        return section_tasks

    @classmethod
    def get_project_collaborators(cls, project_name:str):
        project_id = cls.get_project_from_name(project_name).id
        return cls.api.get_collaborators(project_id)

class TASK_MAP(Enum):
    COLLABORATOR = auto()
    SECTION = auto()
    LABEL = auto()

# TODO in use?
def get_task_ids(tasks:list):
    return [task.id for task in tasks]

class Project:
    def __init__(self, project_name:str):
        self.project_name = project_name
        self.project = todoist_client.get_project_from_name(project_name)

        sections = {section.id: section for section in todoist_client.get_project_sections(project_name)}
        collaborators = {collaborator.id: collaborator for collaborator in todoist_client.get_project_collaborators(project_name)}

        collaborator_task_map= {collaborator_id: [] for collaborator_id in collaborators}
        self.tasks = {task.id: task for task in todoist_client.get_project_tasks(project_name)}
        for task_id, task_value in self.tasks.items():
            if task_value.assignee_id is not None:
                collaborator_task_map[task_value.assignee_id].append(task_id)

        section_task_map = {section: todoist_client.get_section_task_ids(section) for section in sections}

        self.task_maps = {
            TASK_MAP.COLLABORATOR: collaborator_task_map,
            TASK_MAP.SECTION: section_task_map
        }

        self.id_to_instance_map = {
            TASK_MAP.COLLABORATOR: collaborators,
            TASK_MAP.SECTION: sections
        }

    def get_instance_by_name(self, map_key:TASK_MAP, name:str):
        for class_instace in self.id_to_instance_map[map_key].values():
            if class_instace.name == name:
                return class_instace

    def get_section_by_name(self, section_name:str):
        map_key = TASK_MAP.SECTION
        return self.get_instance_by_name(map_key, section_name)

    def get_collaborator_by_name(self, collaborator_name:str):
        map_key = TASK_MAP.COLLABORATOR
        return self.get_instance_by_name(map_key, collaborator_name)

    def get_tasks_by_ids(self, task_ids:list):
        return [self.tasks[task_id] for task_id in task_ids]

    def filter_map(self, map_type:TASK_MAP, filter_functions:list):
        """
        Filters a map by a list of filter functions

        Args:
            map_type (TASK_MAP): The type of map to filter
            filter_functions (list): A list of tuples containing the filter function and the arguments to pass to it
        """
        filtered_map = {}
        for map_key, task_ids in self.task_maps[map_type].items():
            tasks = self.get_tasks_by_ids(task_ids)
            for filter_function, function_arg in filter_functions:

                if isinstance(function_arg, dict) == False:
                    raise Exception('Filter function arguments must be passed as a dictionary')

                if callable(filter_function) == False:
                    raise Exception('Filter function must be callable')

                tasks = filter_function(tasks, **function_arg)

            filtered_map[map_key] = get_task_ids(tasks)

        return filtered_map

def print_map(input_map:dict, map_source:Project, map_type:TASK_MAP, verbose=False):
    key_object = map_source.id_to_instance_map[map_type]
    for input_key, input_task_id in input_map.items():
        print(key_object[input_key].name)
        for task_id in input_task_id:
            task = map_source.tasks[task_id]
            print(f'\t{task.content}')
            if verbose:
                print(f'\t\t{task.description}')
