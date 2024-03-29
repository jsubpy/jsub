import os
import logging

from jsub.loader import load_class

from jsub.util import snake_to_camel

from jsub.config.error import UnknownConfigFormatError
from jsub.config.error import ConfigFileNotFoundError


_GUESS_CONFIG_FORMAT = ('yaml', 'json', 'toml', 'py')

_jsub_logger = logging.getLogger('JSUB')


def _file_ext(fn):
	file_ext = os.path.splitext(fn)[1]
	if file_ext.startswith('.'):
		return file_ext[1:]
	return file_ext

def _config_handler(fmt):
	config_type = fmt + '_config'
	config_class = snake_to_camel(config_type)
	return load_class('jsub.config.handler.'+config_type, config_class)()

def _load_config(s, fmt):
	config_handler = _config_handler(fmt)
	return config_handler.load_str(s)

def _load_config_guess(s):
	for fmt in _GUESS_CONFIG_FORMAT:
		try:
			return _load_config(s, fmt)
		except Exception:
			_jsub_logger.debug('Skip config format : %s' % fmt)
			continue
	raise UnknownConfigFormatError('Do not know the config string format')


def load_config_string(s, fmt=''):
	if fmt:
		return _load_config(s, fmt)
	return _load_config_guess(s)

def load_config_file(fn, fmt=''):
	if not os.path.exists(fn):
		return {}
	with open(fn, 'r') as f:
		file_content = f.read()
		file_content = file_content.replace('\t','  ')	# allow \t in yaml

	config_format = ''
	if fmt:
		config_format = fmt
	elif _file_ext(fn) in _GUESS_CONFIG_FORMAT:
		config_format = _file_ext(fn)

	try:
		return load_config_string(file_content, config_format)
	except UnknownConfigFormatError:
		raise UnknownConfigFormatError('Do not know the config file format: %s' % fn)

def find_and_load_config_file(directory, name):
	for fn in os.listdir(directory):
		full_path = os.path.join(directory, fn)
		if os.path.splitext(fn)[0] == name and os.path.isfile(full_path):
			try:
				return load_config_file(full_path)
			except Exception as e:
				_jsub_logger.debug('Skip unknown config file "%s": %s' % (full_path, e))
				continue

	raise ConfigFileNotFoundError('Config "%s" not found in directory "%s"' % (name, directory))

def dump_config_string(config, fmt):
	config_handler = _config_handler(fmt)
	return config_handler.dump_str(config)

def dump_config_file(config, fn, fmt):
	config_handler = _config_handler(fmt)
	return config_handler.dump_file(config, fn)
