import os
import logging

class Getlog(object):
	def __init__(self, manager, task_id, sub_id, status, njobs, path = ''):
		self.__manager = manager
		self.__backend_mgr = self.__manager.load_backend_manager()
		self.__task_id = task_id	
		self.__status = status		# filter the status of jobs
		if njobs is not None:		# max number of jobs for log retrieval
			self.__njobs = njobs		
		else:
			self.__njobs = 10
		self.__task = self.__manager.load_task(task_id)

		try:						# filter the sub_ids of jobs
			self.__sub_id = sub_id.split(',')
		except:
			self.__sub_id = ['']
		for i in range(len(self.__sub_id)):
			try:
				self.__sub_id[i]=int(self.__sub_id[i])
			except:
				self.__sub_id.pop(i)
		if path =='':
			run_root = self.__backend_mgr.get_run_root(self.__task.data['backend'], self.__task.data['id'])
			self.__path = os.path.join(run_root,'../logfiles')
		else:
			self.__path = path
		self.__logger = logging.getLogger('JSUB')

	def handle(self):
		status = []
		for s in ['Done','Waiting','Running','Failed','Deleted']:
			if s in self.__status:
				status.append(s)
			elif s == 'Done':
				if ('D' in self.__status) and (self.__status.lower().find('delete')<0):
					status.append(s)
			else:
				if s == 'Deleted':
					s0 = 'O'
				else:
					s0 = s[0]
				if s0 in self.__status:
					status.append(s)

		getlog_result = self.__backend_mgr.get_log(self.__task.data['backend'],  task_data = self.__task.data, path = self.__path, sub_ids = self.__sub_id , status = status, njobs = self.__njobs)
		for sid in getlog_result:
			if getlog_result[sid]['OK']==False:
				self.__logger.info('Failed to get the log file of subjob %s: %s'%(sid,getlog_result[sid]['Message']))
