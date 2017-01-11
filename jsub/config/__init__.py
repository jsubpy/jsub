import os

from jsub.error import JsubError

from jsub.loader import load_class

from jsub.util import snake_to_camel


_GUESS_CONFIG_FORMAT = ('yaml', 'json', 'toml', 'py')


class UnknownConfigFormatError(JsubError):
    pass


def _file_ext(fn):
    file_ext = os.path.splitext(fn)[1]
    if file_ext.startswith('.'):
        return file_ext[1:]
    return file_ext

def _config_handler(fmt):
    config_type = fmt + '_config'
    config_class = snake_to_camel(config_type)
    return load_class('jsub.config.'+config_type, config_class)()

def _load_config(s, fmt):
    config_handler = _config_handler(fmt)
    return config_handler.load_str(s)

def _guess_format(s):
    for fmt in _GUESS_CONFIG_FORMAT:
        try:
            _load_config(s, fmt)
            return fmt
        except:
            continue
    raise UnknownConfigFormatError('Do not know the config string format')


def load_config_string(s, fmt=''):
    if fmt:
        config_format = fmt
    else:
        config_format = _guess_format(s)

    return _load_config(s, config_format)

def load_config_file(fn, fmt=''):
    with open(fn, 'r') as f:
        file_content = f.read()

    if fmt:
        config_format = fmt
    else:
        config_format = _file_ext(fn)

    try:
        return load_config_string(file_content, config_format)
    except UnknownConfigFormatError:
        raise UnknownConfigFormatError('Do not know the config file format: %s' % fn)

def dump_config_string(config, fmt):
    config_handler = _config_handler(fmt)
    return config_handler.dump_str(config)
