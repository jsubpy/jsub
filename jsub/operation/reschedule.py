import logging

class Reschedule(object):
	def __init__(self, manager, task_id, status='', sub_id=None, backend_id=None):
		self.__manager = manager
		self.__backend_mgr = self.__manager.load_backend_manager()
		self.__task = self.__manager.load_task(task_id)
		self.__status = status
		self.__sub_ids = sub_id
		self.__backend_ids = backend_id	
		self.__task_id = task_id
		self.__logger = logging.getLogger('JSUB')

	def handle(self):
		backend_task_id = self.__task.data.get('backend_task_id')
		result = {}
		if not backend_task_id:
			self.__logger.info('Cannot retrieve task information on backend, failed to reschedule.')
			return None
		backend_job_ids=self.__task.data.get('backend_job_ids',{})

		if self.__status:
			status = []
			for s in ['Waiting','Failed','Done','Running']:
				if s[0] in self.__status:
					status.append(s)
			self.__logger.info('Resubmitting jobs with %s status(es) in Task %d.'%(status,self.__task_id))
			result = self.__backend_mgr.reschedule(self.__task.data['backend'], backend_task_id, status = status)

		elif self.__sub_ids: #map sub_id with backend_id and reschedule according to backend_ids
			backend_ids=[]
			for sid in self.__sub_ids:
				bid = backend_job_ids.get(sid)
				bid = backend_job_ids.get(str(sid),bid)
				if bid:
					backend_ids.append(bid)
			self.__logger.info('Resubmitting jobs with selected sub-ids in Task %d.'%self.__task_id)
			result = self.__backend_mgr.reschedule(self.__task.data['backend'], backend_task_id, backend_ids = backend_ids)
			
		elif self.__backend_ids: 
			
			self.__logger.info('Resubmitting jobs with selected backend-ids in Task %d.'%self.__task_id)
			result = self.__backend_mgr.reschedule(self.__task.data['backend'], backend_task_id, backend_ids = self.__backend_ids)

		else:
			self.__logger.info('No valid status from Done/Failed/Running/Waiting is selected for reschedule command.')

		if result.get('OK'):
			if isinstance(result['Value'], dict):
				length=len(result['Value'].get('JobID',[]))
			elif isinstance(result['Value'], list):
				length=len(result['Value'])
			else:
				length=0
			self.__logger.info('Successfully rescheduled %d jobs.'%length)

			self.__task.data['status']='Rescheduled'
			task_pool = self.__manager.load_task_pool()
			task_pool.save(self.__task)
		
	
