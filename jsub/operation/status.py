import os
import logging

class Status(object):
	def __init__(self, manager, task_id, states=None, silent=False):
		self.__manager = manager
		self.__backend_mgr   = self.__manager.load_backend_manager()
		self.__silent = silent
		self.__states= states

		self.__task = self.__manager.load_task(task_id)
		self.__task_id = task_id
	
		self.__logger = logging.getLogger('JSUB')

	def handle(self):
		backend_task_id = self.__task.data.get('backend_task_id')
		njobs_txt=''		#D|F|W|R|O
		report=''	
		if backend_task_id:
			# backend_status in format 	{'OK': True/False, 'njobs': {state: njobs}, 'jobIDs':{state: [jobID]}}
			backend_status=self.__backend_mgr.status(self.__task.data['backend'], backend_task_id, states=self.__states,silent=self.__silent)		
			self.__logger.debug(backend_status)
			try:
				if backend_status['OK']:		
					pass
			except:
				backend_status={'OK':False,'Message':'Invalid result.'}
			if backend_status['OK']:
				if 'njobs' in backend_status:
					njobs=backend_status['njobs']
					report='Total jobs: %s'%njobs['Total']
					for t in ['Done','Failed','Running','Waiting','Deleted']:
						if njobs[t]>0:
							report+=', %s: %s'%(t,njobs[t])
						njobs_txt+='%d|'%(njobs[t])
					njobs_txt=njobs_txt[0:-1]	

				if 'jobIDs' in backend_status:
					jobIDs=backend_status['jobIDs']
					for status in jobIDs:
						idlist=[]
						for target_bid in jobIDs[status]:
							for jid,bid in self.__task.data.get('backend_job_ids',{}).items():
								if bid==target_bid:
									idlist.append('%s:%s'%(jid,bid))
						self.__logger.info('There are %d jobs with status %s:\n%s'%(len(jobIDs[status]),status,', '.join(idlist)))
			else:
				report = 'Failed to retrieve %s backend status for task %s.'%(self.__task.data['backend'].get('type','backend'), self.__task_id)
				
		else:
			if self.__task.data['status']=='New':
				report='The task has not been submitted yet.'
			else:
				report='Cannot retrieve the info of JSUB task %s on %s backend: there is no valid backend task ID. (Bad submission?)'%(self.__task_id, self.__task.data['backend']['type'])

		if (not self.__silent) and report:
			self.__logger.info(report)

		if self.__task.data['status']!='New' and njobs_txt:
			self.__task.data['status']=njobs_txt
			task_pool = self.__manager.load_task_pool()
			task_pool.save(self.__task)
