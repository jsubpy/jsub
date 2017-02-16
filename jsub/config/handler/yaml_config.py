import yaml

class YamlConfig(object):
    def __init__(self, param={}):
        pass

    def load_file(self, fn):
        with open(fn, 'r') as f:
            return yaml.load(f)

    def load_str(self, s):
        return yaml.load(s)

    def dump_file(self, data, fn):
        with open(fn, 'w') as f:
            yaml.dump(data, f)

    def dump_str(self, data):
        return yaml.dump(data)
