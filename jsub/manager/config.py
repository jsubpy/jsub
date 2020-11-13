from jsub.config		import load_config_file
from jsub.manager.error import BackendNotSetupError
import os
from jsub.util import deep_update
import collections, sys
import copy

JSUB_MAIN_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../')


class ConfigManager(object):
	default_settings = {
		'log_level': 'INFO',
		'runDir': '~/jsub/run',
		'max_cycle': 10000,
	}

	def __init__(self, schema_mgr, jsubrc):
		self.__schema_mgr = schema_mgr
		# use .jsubrc in JSUB main dir for default configuration
		default_jsubrc = self.__schema_mgr.validate_jsubrc_config(load_config_file(os.path.join(JSUB_MAIN_DIR,'.jsubrc')))
		# and deep-update with user's configuration
		user_jsubrc = self.__schema_mgr.validate_jsubrc_config(load_config_file(jsubrc))
		updated_jsubrc= self.merge_config(default_jsubrc, user_jsubrc)

		self.__config_jsubrc = updated_jsubrc
		self.__config = self.__config_jsubrc

	def merge_config(self,default_conf, user_conf):
		result = copy.deepcopy(default_conf)
		pkg_list=result.get('package',[])
		pkg_list.extend(user_conf.get('package',[]))
		deep_update(result, user_conf)
		result['package'] = copy.deepcopy(pkg_list)
		return result

	def merge_packages_config(self, packages_config):
		pass

	def config_jsubrc(self, item):
		if item in self.__config_jsubrc:
			return self.__config_jsubrc[item]
		if item in default_settings:
			return default_settings[item]
		raise ConfigNotSetupError('Configuration not found for: %s' % item)


	def config(self, item):
		return self.config_jsubrc(item)

	def repo(self): #task data repository
		config_repo = {}			
		config_repo['type'] = 'file_system'
		config_repo['param'] = {'dir': '~/jsub/taskInfo/', 'format': 'compact'}

		if 'taskDir' in self.__config:
			taskDir=self.__config['taskDir'].get('location','~/jsub/')
			repo_dir=os.path.join(taskDir,'taskInfo/')

			if 'repo' in self.__config['taskDir']:
				config_repo['param']=self.__config['taskDir']['repo']				
				config_repo['type']=self.__config['taskDir']['repo'].get('type','file_system')

			config_repo['param']['repoDir']=repo_dir		#old folder structure
			config_repo['param']['taskDir']=taskDir

		return config_repo

	def content(self): #raw task data
		config_content = {}
		config_content['type'] = 'file_system'
		config_content['param'] = {'dir': '~/jsub/taskInfo/'}

		if 'taskDir' in self.__config:
			taskDir=self.__config['taskDir'].get('location','~/jsub/')
			content_dir=os.path.join(taskDir,'taskInfo/')	

			if 'content' in self.__config['taskDir']:
				config_content['param']=self.__config['taskDir']['content']				
				config_content['type']=self.__config['taskDir']['content'].get('type','file_system')				

			config_content['param']['contentDir']=content_dir	#old folder structure
			config_content['param']['taskDir']=taskDir
		return config_content

	def bootstrap(self):
		if 'bootstrap' in self.__config:
			return self.__config['bootstrap']
		return 'shell'

	def navigator(self):
		if 'navigator' in self.__config:
			return self.__config['navigator']
		return ['python']


	def task_name(self, task_profile):
		name=task_profile.get('experiment')
		name=task_profile.get('scenario',name)
		name=task_profile.get('name',name)
		name=task_profile.get('taskName',name)
		return name


	def scenario_data(self, task_profile):
		# users may specify scenario_type with scenario/experiment tag
		scenario_type = task_profile.get('scenario', 'common')
		scenario_type = task_profile.get('experiment', scenario_type)
		# users may put attributes inside or outside param block
		scenario_param = copy.deepcopy(task_profile)
		try:
			scenario_param.pop('param')
		except:
			pass
		scenario_param.update(task_profile.get('param', {}))
		return {'type': scenario_type, 'param': scenario_param}


	def backend_data(self, task_profile):
		backend_param_profile={}
		if 'backend' not in task_profile:
			try:
				backend_name = self.__config['backend']['default']
			except KeyError:
				raise BackendNotSetupError('Must specify a backend')
		else:
			backend_in_profile = task_profile['backend']
			if isinstance(backend_in_profile, str):
				backend_name = backend_in_profile
				backend_in_profile = {'type':backend_name}
			elif isinstance(backend_in_profile, dict):
				if 'type' not in backend_in_profile:
					raise BackendNotSetupError('Must specify the backend type')
				backend_name = backend_in_profile['type']
				backend_param_profile = backend_in_profile.get('param',{})
			else:
				raise BackendNotSetupError('Backend value format not correct')

		# Load backend setting from jsubrc
		backend_type = self.__config.get('backend', {}).get(backend_name, {}).get('type', backend_name)
		backend_launcher = self.__config.get('backend', {}).get(backend_name, {}).get('launcher', 'arg')
		backend_param = self.__config.get('backend', {}).get(backend_name, {}).get('param', {})
		# in jsubrc: load attributes outside param block
		backend_o = self.__config.get('backend',{}).get(backend_name,{})	
		backend_oparam = copy.deepcopy(backend_o)
		try:
			backend_oparam.pop('param')
		except:
			pass
		backend_param.update(backend_oparam)

		# users may put attributes inside or outside param block
		backend_param_po = copy.deepcopy(backend_in_profile)
		try:
			backend_param_po.pop('param')
		except:
			pass
		backend_param_profile.update(backend_param_po)
	
		# try overloading setting from task profile
		backend_param.update(backend_param_profile)

		if 'runDir' not in backend_param:
			if 'taskDir' in self.__config:
				taskDir=self.__config['taskDir'].get('location','~/jsub/')
				backend_param['runDir']=os.path.join(taskDir,'run')
				backend_param['taskDir']=taskDir
			else:
				backend_param['runDir'] = self.__config['backend'].get('runDir', '~/jsub/run')
				backend_param['taskDir'] = self.__config['backend'].get('taskDir', '~/jsub')

		if 'jobName' not in backend_param:
			backend_param['jobName']=task_profile.get('taskName','')
			

		return {'type': backend_type, 'launcher': backend_launcher, 'param': backend_param}
