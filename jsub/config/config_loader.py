import os
import copy
import collections

from jsub.config.yaml_loader import load as yaml_load


DEFAULT_CONFIG_FILE = os.path.expanduser('~/.jsubrc')

def load_default():
    default_config = yaml_load(DEFAULT_CONFIG_FILE)
    return default_config


def _update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d

def load_config(config_file):
    return yaml_load(config_file)

def merge(base_config, config):
    final_config = copy.deepcopy(base_config)
    update(final_config, config)
    return final_config
