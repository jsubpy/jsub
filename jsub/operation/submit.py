import os
import logging

from jsub.util import safe_mkdir
from jsub.util import safe_rmdir

class Submit(object):
	def __init__(self, manager, task_id, sub_ids=None, dry_run=False, resubmit=False):
		self.__manager = manager
		self.__task	= self.__manager.load_task(task_id)
		self.__sub_ids = sub_ids
		self.__dry_run = dry_run
		self.__resubmit = resubmit

		self.__logger = logging.getLogger('JSUB')
		if self.__sub_ids==None:
			self.__sub_ids=range(len(self.__task.data['jobvar']))

		self.__initialize_manager()

	def __initialize_manager(self):
		self.__config_mgr	= self.__manager.load_config_manager()

		self.__backend_mgr   = self.__manager.load_backend_manager()
		self.__bootstrap_mgr = self.__manager.load_bootstrap_manager()
		self.__navigator_mgr = self.__manager.load_navigator_manager()
		self.__context_mgr  = self.__manager.load_context_manager()
		self.__action_mgr	= self.__manager.load_action_manager()
		self.__launcher_mgr  = self.__manager.load_launcher_manager()


	def handle(self):
		run_root = self.__backend_mgr.get_run_root(self.__task.data['backend'], self.__task.data['id'])

		main_root = os.path.join(run_root, 'main')

		safe_rmdir(main_root)
		safe_mkdir(main_root)

		self.__create_input(main_root)
		self.__create_context(main_root)
		self.__create_action(main_root)
		self.__create_navigator(main_root)
		self.__create_bootstrap(main_root)

		launcher_param = self.__create_launcher(run_root)

		self.__submit(launcher_param)


	def __create_input(self, main_root):
		content = self.__manager.load_content()
		input_dir = os.path.join(main_root,'input')
		try:
			content.get(self.__task.data['id'], 'input', os.path.join(main_root, 'input'))
		except:
			safe_mkdir(input_dir)

	def __create_context(self, main_root):
		context_dir = os.path.join(main_root, 'context')
		safe_mkdir(context_dir)

		action_default = {}
		for unit, param in self.__task.data['workflow'].items():
			action_default[unit] = self.__action_mgr.default_config(param['type'])

		navigators = self.__config_mgr.navigator()
		context_format = self.__navigator_mgr.context_format(navigators)

		self.__context_mgr.create_context_file(self.__task.data, action_default, context_format, context_dir)

	def __create_action(self, main_root):
		action_dir = os.path.join(main_root, 'action')
		safe_mkdir(action_dir)

		actions = set()
		for unit, param in self.__task.data['workflow'].items():
			actions.add(param['type'])
		self.__action_mgr.create_actions(actions, action_dir)

	def __create_navigator(self, main_root):
		navigator_dir = os.path.join(main_root, 'navigator')
		safe_mkdir(navigator_dir)

		navigators = self.__config_mgr.navigator()
		self.__navigator_mgr.create_navigators(navigators, navigator_dir)

	def __create_bootstrap(self, main_root):
		bootstrap_dir = os.path.join(main_root, 'bootstrap')
		safe_mkdir(bootstrap_dir)

		bootstrap = self.__config_mgr.bootstrap()
		self.__bootstrap_mgr.create_bootstrap(bootstrap, bootstrap_dir)

	def __create_launcher(self, run_root):
		launcher = self.__task.data['backend']['launcher']
		return self.__launcher_mgr.create_launcher(launcher, run_root)


	def __submit(self, launcher_param):
		if self.__dry_run:
			return

		if self.__resubmit==False:
			if self.__task.data.get('backend_job_ids') or self.__task.data.get('backend_task_id'):
				self.__logger.info('This task has already been submitted to backend, rerun the command with "-r" option if you wish to delete current jobs and resubmit the task.') 
				return
		else:	
			self.__logger.info('Removing submitted jobs on backend before resubmission.') 
			task_id = self.__task.data.get('backend_task_id')
			#remove previously generated files in job folder
			job_ids = self.__task.data.get('backend_job_ids')
			run_root = self.__backend_mgr.get_run_root(self.__task.data['backend'], self.__task.data['id'])
			job_root=os.path.join(run_root,'subjobs')
			safe_rmdir(job_root)
			if task_id:
				self.__backend_mgr.delete_task(self.__task.data['backend'],backend_task_id = task_id)
			elif job_ids:
				self.__backend_mgr.delete_jobs(self.__task.data['backend'],backend_job_ids = job_ids)

		result = self.__backend_mgr.submit(self.__task.data['backend'], self.__task.data['id'], launcher_param, sub_ids = self.__sub_ids)
		if not type(result) is  dict:
			result = {}

		if 'backend_job_ids' in result:
			njobs = len(result['backend_job_ids'])
		else:
			njobs = len(result)
		if njobs>0:
			self.__logger.info('%d jobs successfully submitted to backend.'%(njobs))

		self.__task.data.setdefault('backend_job_ids',{})
		backend_job_ids=result.get('backend_job_ids',{})
		backend_task_id=result.get('backend_task_id',0)
		self.__task.data['backend_job_ids'].update(backend_job_ids) 
		self.__task.data['backend_task_id']=backend_task_id
		self.__task.data['status'] = 'Submitted'
		task_pool = self.__manager.load_task_pool()
		task_pool.save(self.__task)

		self.__logger.debug(result)

