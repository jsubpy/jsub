import os
import logging

from jsub.config import dump_config_string
from jsub.util import safe_rmdir

class Create(object):
	def __init__(self, manager, task_profile):
		self.__manager	  = manager
		self.__task_profile = task_profile
		self.__logger = logging.getLogger('JSUB')

		self.__initialize_manager()

	def __initialize_manager(self):
		self.__config_mgr  = self.__manager.load_config_manager()

		self.__scenario_mgr	 = self.__manager.load_scenario_manager()
		self.__seq_mgr	 = self.__manager.load_seq_manager()
		self.__backend_mgr = self.__manager.load_backend_manager()


	def handle(self):
		task_name = self.__config_mgr.task_name(self.__task_profile)

		backend_data = self.__config_mgr.backend_data(self.__task_profile)
		backend_property = self.__backend_mgr.property(backend_data)

		scenario_data = self.__config_mgr.scenario_data(self.__task_profile)
		scenario_result = self.__scenario_mgr.build(scenario_data, backend_property)
		scenario_input = scenario_result.get('input',	 {})
		workflow  = scenario_result.get('workflow',  {})
		prop	  = scenario_result.get('prop',	  {})
		splitter_param = scenario_result.get('splitter', {})

#		jobvar = self.__seq_mgr.split(splitter.get('jobvar_lists',{}),mode = splitter.get('mode','default'), max_cycle = splitter.get('max_subjobs',100000))
		jobvar = self.__seq_mgr.split(splitter_param)		# jobvar = [ [vars for subjob 1], [vars for subjob 2], ... ]

		task_data = {}
		task_data['name']	   = task_name
		task_data['scenario']		= scenario_data
		task_data['workflow']   = workflow
		task_data['event']	  = {}
		task_data['prop']	   = prop
		task_data['splitter']  = splitter_param
		task_data['jobvar']	 = jobvar
		task_data['input_file'] = list(scenario_input.keys())
		task_data['backend']	= backend_data
		task_data['status']	 = 'New'


		task = self.__create_task(task_data)
		task_id = task.data['id']


		try:	# in case file not found error
			self.__copy_input_file(task_id, scenario_input)
			self.__dump_task_profile(task_id)
		except Exception as e:
			self.__logger.error('Failed to create jsub task, error with create input sandbox: %s'%str(e.args))
			self.__delete_task(task_id)
			# avoid printing success message
			return None


		return task


	def __create_task(self, task_data):
		task_pool = self.__manager.load_task_pool()
		return task_pool.create(task_data)

	def __delete_task(self, task_id):
		task_pool = self.__manager.load_task_pool()
		return task_pool.delete(task_id)
		

	def __copy_input_file(self, task_id, scenario_input):
		content = self.__manager.load_content()

		if 'common' in scenario_input:
			for dst, src in scenario_input['common'].items():
				content.put(task_id, src, os.path.join('input', 'common', dst))

		if 'unit' in scenario_input:
			for unit, unit_file_pair in scenario_input['unit'].items():
				for dst, src in unit_file_pair.items():
					content.put(task_id, src, os.path.join('input', 'unit', unit, dst))

	def __dump_task_profile(self, task_id):
		content = self.__manager.load_content()
		content.put_str(task_id, dump_config_string(self.__task_profile, 'yaml'), os.path.join('profile', 'origin'))
