import json

class JsonConfig(object):
    def __init__(self, param={}):
        pass

    def load_file(self, fn):
        with open(fn, 'r') as f:
            return json.load(f)

    def load_str(self, s):
        return json.loads(s)

    def dump_file(self, data, fn):
        with open(fn, 'w') as f:
            json.dump(data, f)

    def dump_str(self, data):
        return json.dumps(data)
