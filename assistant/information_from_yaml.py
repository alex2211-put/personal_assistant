import yaml
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_name():
    with open(_BASE_DIR + '/settings.yaml') as file:
        parameters = yaml.safe_load(file)
    return parameters.get('name')


def set_name(name):
    with open(_BASE_DIR + '/settings.yaml', 'r') as file:
        parameters = yaml.safe_load(file)
    if not parameters:
        parameters = {}
    parameters['name'] = name
    with open(_BASE_DIR + '/settings.yaml', 'w') as file:
        yaml.dump(parameters, file)
