from jsub.manager.error import JobvarListNotSetupError
import copy
import re

#translate jobvar_single (from jobvar extension) according to name_map (from task profile)
def _jobvar_name_map(jobvar_single, name_map):
	jobvar_new = {}
	for k, v in jobvar_single.items():
		if k in name_map:
			jobvar_new[name_map[k]] = v
		else:
			jobvar_new[k] = v
	return jobvar_new


class SplitterManager(object):
	def __init__(self, ext_mgr):
		self.__ext_mgr = ext_mgr

	def split(self, splitter_info):
		#generate jobvar
		self.__info = splitter_info
		mode = splitter_info.get('mode','SplitByJobvars')
		mode = splitter_info.get('type',mode)
		mode = re.sub(r'(?<!^)(?=[A-Z])','_', mode).lower()		#camel to snake case
		self.__info['type'] = mode
		self.__info['ext_mgr']=self.__ext_mgr
		params = copy.deepcopy(self.__info) # put attributes under info.param; for extension manager

		self.__info['param'] = params
		

		splitter=self.__ext_mgr.load_ext_common('splitter', self.__info)
		self.__info.pop('ext_mgr')
		
		return splitter.split()

