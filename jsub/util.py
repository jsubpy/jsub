import os
import shutil
import collections, sys
import logging

def camel_to_snake(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def snake_to_camel(name):
	return name.title().replace('_', '')


def safe_rmdir(directory):
	if os.path.isdir(directory):
		shutil.rmtree(directory)

def safe_mkdir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def safe_copy(src, dst):
	if not os.path.exists(dst):
		directory = os.path.dirname(dst)
		safe_mkdir(directory)
	shutil.copy2(src, dst)


def expand_path(path):
	temp_path = os.path.expanduser(path)
	temp_path = os.path.expandvars(temp_path)
	return os.path.normpath(temp_path)


def ensure_list(item):
	return item if isinstance(item, list) else [item]

def unique_list(seq):
	unique = []
	for item in seq:
		if item not in unique:
			unique.append(item)
	return unique


def deep_update(orig_dict, new_dict):
	if sys.version_info[0] < 3: #for python 2
		for key, val in new_dict.iteritems():
			if isinstance(val, collections.Mapping):
				tmp = deep_update(orig_dict.get(key, { }), val)
				orig_dict[key] = tmp
			elif isinstance(val, list):
				orig_dict[key] = (orig_dict.get(key, []) + val)
			else:
				orig_dict[key] = new_dict[key]
		return orig_dict
	else:	# python 3 version
		for k, v in new_dict.items():
			if isinstance(v, collections.abc.Mapping):
				orig_dict[k] = deep_update(orig_dict.get(k, {}), v)
			else:
				orig_dict[k] = v
		return orig_dict


	
