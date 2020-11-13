import os

from jsub.manager   import Manager
from jsub.operation import Operation


JSUB_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def version():
	with open(os.path.join(JSUB_ROOT_DIR, 'VERSION'), 'r') as f:
		ver = f.read()
	return ver.strip()


class Jsub(object):
	def __init__(self, jsubrc='~/.jsubrc'):
		self.__manager = Manager(jsubrc)
		self.__operation = None

	def package(self):
		return self.__manager.load_pkg_manager().packages

	def config(self):
		return self.__manager.load_config_manager().config()


	def __load_operation(self):
		if self.__operation is None:
			self.__operation = Operation(self.__manager)
		return self.__operation


	def rename(self, task_id, new_name):
		op = self.__load_operation()
		return op.rename(task_id, new_name)

	def create(self, task_profile):
		op = self.__load_operation()
		return op.create(task_profile)

	def submit(self, task_id, sub_ids=None, dry_run=False, resubmit=False):
		op = self.__load_operation()
		return op.submit(task_id, sub_ids, dry_run, resubmit)

	def remove(self, task_id, force=False):
		op = self.__load_operation()
		return op.remove(task_id, force)

	def ls(self, task_id=None, update=False):
		op = self.__load_operation()
		return op.ls(task_id, update)

	def show(self, task_id, dump):
		op = self.__load_operation()
		return op.show(task_id, dump)

	def status(self, task_id, states=None, silent=False):
		op = self.__load_operation()
		return op.status(task_id, states, silent)

	def getlog(self, task_id, sub_id, status, njobs, path='./'):
		op = self.__load_operation()
		return op.getlog(task_id, sub_id, status, njobs, path)

	def reschedule(self, task_id, status, sub_id, backend_id):
		op = self.__load_operation()
		return op.reschedule(task_id, status, sub_id, backend_id)

	def merge(self, task_id):
		op = self.__load_operation()
		return op.merge(task_id)

	def output(self, task_id):
		op = self.__load_operation()
		return op.output(task_id)

	def export(self, task_id, task_sub_id=[], output_dir='.', task_profile_format='yaml'):
		''' Export job files (task_profile and input) for a task/job
			User can modify the files and submit again, with a common scenario
		'''
		op = self.__load_operation()
		return op.recreate(task_id=task_id, task_sub_id=task_sub_id, output_dir=output_dir, task_profile_format=task_profile_format)
