from jsub.error import TaskIdFormatError
from jsub.operation.status import Status

def _convert_tasks_data(tasks):
	tasks_data = []
	for task in tasks:
		tasks_data.append(task.data)
	return tasks_data

class Ls(object):
	def __init__(self, manager, task_id=None, update=False):
		self.__manager = manager
		self.__task_id = task_id
		self.__update = update

		self.__initialize_manager()

	def __initialize_manager(self):
		self.__config_mgr   = self.__manager.load_config_manager()


	def handle(self):
		task_pool = self.__manager.load_task_pool()

		if self.__task_id is None:
			return self.__all_tasks()

		if isinstance(self.__task_id, (int, list)):
			return self.__find_tasks(self.__task_id)

		raise TaskIdFormatError('Unknown task ID format: %s' % self.__task_id)


	def __all_tasks(self):
		task_pool = self.__manager.load_task_pool()
		all_tasks=task_pool.all()
		if self.__update:
			for task in all_tasks:	#update task status
				Status(self.__manager,task.data['id'], silent=True).handle()
		return _convert_tasks_data(task_pool.all())

	def __find_tasks(self, task_ids):
		task_pool = self.__manager.load_task_pool()
		if self.__update:
			for i in task_ids:		#update task status
				Status(self.__manager, i, silent=True).handle()
		return _convert_tasks_data(task_pool.find(task_ids))
