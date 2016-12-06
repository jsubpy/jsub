import toml

def file_ext():
    return ['toml']

def load(config_file):
    with open(config_file, 'r') as f:
        return toml.load(f.read())
