import yaml
import os
from . import utils


data_map = None


def get_value(name):
    return data_map[name]


def add_value(name, value):
    data_map[name] = value
    with utils.resource('config.yaml', 'w') as f:
        yaml.dump(dataMap, f, default_flow_style=False)


def load_config():
    global data_map
    with utils.resource('config.yaml') as f:
        data_map = yaml.safe_load(f)


load_config()