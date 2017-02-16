import ast

class PyConfig(object):
    def __init__(self, param={}):
        pass

    def load_file(self, fn):
        with open(fn, 'r') as f:
            return ast.literal_eval(f.read())

    def load_str(self, s):
        return ast.literal_eval(s)

    def dump_file(self, data, fn):
        with open(fn, 'w') as f:
            f.write(str(data))

    def dump_str(self, data):
        return str(data)
