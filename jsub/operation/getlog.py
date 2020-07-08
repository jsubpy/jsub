import os
import logging

class Getlog(object):
	def __init__(self, manager, task_id, sub_id = None, path = None):
		self.__manager = manager
		self.__backend_mgr = self.__manager.load_backend_manager()
		self.__task_id = task_id
		self.__task = self.__manager.load_task(task_id)
		try:
			self.__sub_id = sub_id.split(',')
		except:
			self.__sub_id = ['']
		for i in range(len(self.__sub_id)):
			try:
				self.__sub_id[i]=int(self.__sub_id[i])
			except:
				self.__sub_id.pop(i)
		self.__path = path
		self.__logger = logging.getLogger('JSUB')

	def handle(self):
		getlog_result = self.__backend_mgr.get_log(self.__task.data['backend'],  task_data = self.__task.data, path = self.__path, sub_ids = self.__sub_id)
		for sid in getlog_result:
			if getlog_result[sid]['OK']==False:
				self.__logger.info('Failed to get the log file of subjob %s: %s'%(sid,getlog_result[sid]['Message']))
