import os
import copy
import collections

from jsub.config.yaml_loader import load as yaml_load


DEFAULT_CONFIG_FILE = os.path.expanduser('~/.jsubrc')
default_config = {}

def load_default():
    global default_config
    if os.path.isfile(DEFAULT_CONFIG_FILE):
        default_config = yaml_load(DEFAULT_CONFIG_FILE)


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

def merge(config):
    global default_config
    final_config = copy.deepcopy(default_config)
    update(final_config, config)
    return final_config

def load_and_merge(config_file):
    config = yaml_load(config_file)
    return merge(config)
