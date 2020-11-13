import os

class Common(object):
	def initialize_common_param(self):
		self._run_dir = os.path.expanduser(self._param.get('runDir'))
		self._task_dir = os.path.expanduser(self._param.get('taskDir'))

	def get_task_root(self, task_id):
		return os.path.join(self._task_dir, str(task_id))
	def get_run_root(self, task_id):
		return os.path.join(self._task_dir, str(task_id),'runtime')
