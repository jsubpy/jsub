import pytoml as toml

class TomlConfig(object):
    def __init__(self, param={}):
        pass

    def load_file(self, fn):
        with open(fn, 'r') as f:
            return toml.load(f)

    def load_str(self, s):
        return toml.loads(s)

    def dump_file(self, data, fn):
        with open(fn, 'w') as f:
            toml.dump(f, data)

    def dump_str(self, data):
        return toml.dumps(data)
