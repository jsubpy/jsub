import os
import sys
import inspect

from jsub.error import JsubError


class LoadError(JsubError):
	pass

class ModuleNotFoundError(LoadError):
	pass

class ClassNotFoundError(LoadError):
	pass

class NotAClassError(LoadError):
	pass

class PackageDirectoryNotFoundError(LoadError):
	pass


def load_module(module_name):
	
	try:
		__import__(module_name)
	except ImportError as e:
		raise ModuleNotFoundError('Module "%s" not found' % module_name)
	return sys.modules[module_name]


def load_class(module_name, class_name):
	m = load_module(module_name)
	try:
		c = getattr(m, class_name)
	except AttributeError as e:
		raise ClassNotFoundError('Class "%s" not found in module "%s"' % (class_name, module_name))

	if not inspect.isclass(c):
		raise NotAClassError('"%s" in module "%s" is not a class' % (class_name, module_name))

	return c


def package_dir(module_name):
	m = load_module(module_name)
	module_path = m.__file__
	if not os.path.basename(module_path).startswith('__init__.'):
		raise PackageDirectoryNotFoundError('Package directory is not found for module "%s"' % module_name)
	return os.path.dirname(os.path.realpath(module_path))
