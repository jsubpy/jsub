import os
import logging

from jsub.util import safe_rmdir

class Remove(object):
	def __init__(self, manager, task_id, force=False):
		self.__manager = manager
		self.__force = force
		self.__task_id=task_id

		self.__logger = logging.getLogger('JSUB')

		self.__initialize_managers()


	def __initialize_managers(self):
		self.__config_mgr	= self.__manager.load_config_manager()
		self.__backend_mgr   = self.__manager.load_backend_manager()
		
	def handle(self):
		try:
			self.__task = self.__manager.load_task(self.__task_id)
		except:
			self.__logger.info('Failed to remove the task. Wrong task ID?')
			return		

		backend_task_id = self.__task.data.get('backend_task_id')
		backend_job_ids = self.__task.data.get('backend_job_ids')
		
		if backend_task_id or backend_job_ids:
			if not self.__force:
				self.__logger.info('This task has already been submitted to backend, rerun the command with "-f" option if you wish to remove it.')
				return
			else:
				self.__logger.info('Removing task on backend.')
				task_result = self.__backend_mgr.delete_task(self.__task.data['backend'],backend_task_id = backend_task_id)
				if task_result is None:
					task_result = self.__backend_mgr.delete_jobs(self.__task.data['backend'],backend_job_ids = backend_job_ids)

				if (task_result):
					result=task_result['Value']
					result.update({'Backend':self.__task.data['backend']['type']})
					try:
						self.__logger.info('Successfully deleted %d jobs on backend.'%len(result['JobID']))
					except:
						self.__logger.info(result)
				self.__logger.info('Removing runtime files for task.')
		try:
			run_root = self.__backend_mgr.get_run_root(self.__task.data['backend'], self.__task.data['id'])
			safe_rmdir(run_root)
		except:		
			pass

		self.__logger.info('Removing task info files.')
		task_pool = self.__manager.load_task_pool()
		task_pool.delete(self.__task.data['id'])

		self.__logger.info('Task %s successfully removed.'%self.__task.data['id'])


