class BackendManager(object):
	def __init__(self, ext_mgr):
		self.__ext_mgr = ext_mgr

	def property(self, backend_data):
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		return backend.property()

	def get_run_root(self, backend_data, task_id):
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		return backend.get_run_root(task_id)

	def submit(self, backend_data, task_id, launcher_exe, sub_ids = None):
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		submit_result =  backend.submit(task_id, launcher_exe, sub_ids = sub_ids)
		return(submit_result)

	def delete_task(self, backend_data, backend_task_id = 0, job_status = []):
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		try:
			delete_result = backend.delete_task(backend_task_id,job_status)
		except:
			delete_result = None
		return(delete_result)

	def delete_jobs(self, backend_data, backend_job_ids = {}):
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		try:
			delete_result = backend.delete_jobs(backend_job_ids)
		except:
			delete_result = None
		return(delete_result)
	
	def get_log(self, backend_data,  task_data = None, path = None, sub_ids = []):
		'''
		fetch the log files from backend, put to target path.
		getlog_result should return in the format {sub_id:{'OK':True/False,'Message':str}}
		'''
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		try:
			getlog_result = backend.get_log(task_data = task_data, path = path, sub_ids = sub_ids)
		except:
			getlog_result = None
		return(getlog_result)
		

	def reschedule(self, backend_data, backend_task_id = 0, status = None,sub_ids = None, backend_ids = None):
		'''
			reschedule all subjobs according to job status, jsub subIDs, or backend IDs.
			input:
				-status: a list, possible elements include: Done, Waiting, Running, Failed
				-sub_ids: a list of numbers for job IDs
				-backend_ids: a list of numbers for backend job IDs
		'''
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		try:
			reschedule_result = backend.reschedule(backend_task_id,status = status, sub_ids = sub_ids,backend_ids = backend_ids)
		except:
			reschedule_result = {'OK':False,'Message':'Failed to execute reschedule in backend module.'}
		return(reschedule_result)		


	def status(self, backend_data, backend_task_id = 0, states = None):
		'''
			states: a string containing the list of job status users care about:	D/F/R/W/O, Done/Failed/Running/Waiting/Deleted
			status_result:	if failure, return None to operation.status; when successful, return the following dict
			{
				'OK':	True/False,	
				'Message' (if not OK): a string containing the error message, 	
				'Value' (if OK): the num of subjobs in each state,
				'Job_ids' (if states is not None):	{'Running': [id1, id2, ...], ...}
			}
		'''
		backend = self.__ext_mgr.load_ext_common('backend', backend_data)
		try:
			status_result = backend.status(backend_task_id, states) # this is not necessarily supported by every backend
		except:
			status_result = {'OK':False,'Message':'Failed to retrieve info from backend.'}
		return(status_result)
		
