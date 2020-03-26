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


def _expand_jobvar_list(origin, jobvar_name, var_list, max_cycle):
	result=[]
	for var_set in origin:
		for expander in var_list:
			rep=copy.deepcopy(var_set)
			rep[jobvar_name]=expander['value']
			result.append(rep)
			if len(result)>=max_cycle:
				return(result)			

	return(result)



class SplitterManager(object):
	def __init__(self, ext_mgr):
		self.__ext_mgr = ext_mgr

	def split(self, raw_jobvars, max_cycle=100000,mode='shortest'):
		#generate jobvar lists for subjobs, and split subjobs accordingly
		jobvars = []
		compstr_list = []		#the list of jobvars that is of type 'composite_string'

		if not raw_jobvars:
			return jobvars


		raw_jobvar_content = {}
		for jobvar_name, value in raw_jobvars.items():
			if 'type' not in value:
				raise JobvarListNotSetupError('Jobvar list type not setup: %s', jobvar_name)
		
			if value['type'] == 'composite_string':
				compstr_list.append(jobvar_name)
				if mode=='combination':
					value['param']['length']=1

			raw_jobvar_content[jobvar_name] = {}
			raw_jobvar_content[jobvar_name]['instance'] = self.__ext_mgr.load_ext_common('jobvar', value)
			raw_jobvar_content[jobvar_name]['name_map'] = value.get('name_map', {'value':jobvar_name})


		#	if mode='default', split jobs to (var1_1, var2_1), (var1_2, var2_2) ...; length = shortest(len of vars)
		if mode=='default':
			cycle = 0
			while cycle < max_cycle:
				cycle += 1
	
				jobvar = {}
				try:
					for jobvar_name, content in raw_jobvar_content.items():
						jobvar_single = content['instance'].next() 
						jobvar.update(_jobvar_name_map(jobvar_single, content['name_map']))
				except StopIteration:
					break
				jobvars.append(jobvar)
		
		#	if mode='combination' split jobs to (var1_1, var2_1), (var1_1, var2_2) ...; length = len1*len2*len3 ...
		if mode=='combination':
			#translate jobvar description to lists
			jobvar_lists={}
			for jobvar_name, content in raw_jobvar_content.items():
				var_list=[]
				while True:
					try:
						next_value = content['instance'].next() 
						var_list.append(next_value)
					except StopIteration:
						break
				jobvar_lists.update({jobvar_name: var_list})

			#combine the jobvar lists
			jobvars = [{}]
			for jobvar_name, var_list in jobvar_lists.items():
				jobvars = _expand_jobvar_list(jobvars, jobvar_name, var_list, max_cycle)


		#	handling the composite string jobvar
		# 	replace '$(var_name)' with actual values
		if len(compstr_list)>0:
			for idx in range(len(jobvars)):
				jobvar = copy.deepcopy(jobvars[idx])
				
				for key in compstr_list:
					regex='\$\(([^)]+)'
					regex2='\$\{([^}]+)'
					while re.search(regex, jobvar[key]):
						match=re.search(regex, jobvar[key])
						var_name=match.group(0)[2:]
						s=jobvar[key].replace('$('+var_name+')',str(jobvar[var_name]))
						jobvar[key]=s
					while re.search(regex2, jobvar[key]):
						match=re.search(regex2, jobvar[key])
						var_name=match.group(0)[2:]
						s=jobvar[key].replace('${'+var_name+'}',str(jobvar[var_name]))
						jobvar[key]=s

				jobvars[idx]=copy.deepcopy(jobvar)

					

		return jobvars
