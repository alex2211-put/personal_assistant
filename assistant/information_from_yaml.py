import yaml
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_name():
    with open(_BASE_DIR + '/settings.yaml') as file:
        templates = yaml.safe_load(file)
    print(templates)
    return templates.get('name')
