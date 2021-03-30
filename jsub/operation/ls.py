from jsub.error import TaskIdFormatError
from jsub.operation.status import Status
import logging

def _convert_tasks_data(tasks):
	tasks_data = []
	for task in tasks:
		tasks_data.append(task.data)
	return tasks_data

class Ls(object):
	def __init__(self, manager, task_id=None, update=False):
		self.__manager = manager
		self.__task_id = task_id
		self.__do_update = update

		self.__logger = logging.getLogger('JSUB')
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
		if self.__do_update:
			self.__logger.info('Fetching backend status info update for tasks. May take some time.')
			for task in all_tasks:	#update task status
				if  self.__task_need_update(task):
					Status(self.__manager,task.data['id'], silent=True).handle()
		return _convert_tasks_data(task_pool.all())

	def __task_need_update(self,task):
		statuses=task.data['status'].split('|')
		if task.data['backend'].get('type') in ['local']: #skip checking jobs with local backend
			return False
		if len(statuses)<5:	# New/Submitted/Unknown
			if statuses[0] in ['New','Unknown']:
				return False
			else:
				return True	
		elif statuses[2]=='0' and statuses[3]=='0':	# no job in running/waiting status
			return False
		return True


	def __find_tasks(self, task_ids):
		task_pool = self.__manager.load_task_pool()
		if self.__do_update:
			for i in task_ids:		#update task status
				Status(self.__manager, i, silent=True).handle()
		return _convert_tasks_data(task_pool.find(task_ids))
