from jsub.manager.error import JobvarListNotSetupError
import copy
import re

def _jobvar_name_map(jobvar_single, name_map):
	jobvar_new = {}
	for k, v in jobvar_single.items():
		if k in name_map:
			jobvar_new[name_map[k]] = v
		else:
			jobvar_new[k] = v
	return jobvar_new

'''
This splitter generates subjob parameters depending on the input jobvar lists (defined by jobvar extensions).
- Jobvar lists are grouped. For each group, the splitter generates a jobvar-set list with the shortest common length.
- Jobvar-sets in groups other than 'default' are combined, the overall jobvar-set list is the Cartesian product of the lists in groups.
- The jobvars in default group are then put into the combined jobvar-set list to form a final jobvar-set list.
- The number of subjobs to submit is defined by the length of the final jobvar-set list.
- jobvar extension of the type 'compositeString' can reference the values in other jobvars, to form a string.
'''
class SplitByJobvars(object):

	def __init__(self, param):
		self.__ext_mgr = param['ext_mgr']
		self.__param = param
		self.__param.pop('ext_mgr')	#remove the unserializable object

	def split(self):
		raw_jobvars=self.__param.get('jobvars',{})	
		raw_jobvars.update(self.__param.get('jobvarLists',{}))
		raw_jobvars.update(self.__param.get('jobvar_lists',{}))
		max_cycle = self.__param.get('max_subjobs',100000)
		max_cycle = self.__param.get('maxSubjobs',max_cycle)
		max_cycle = self.__param.get('maxSubJobs',max_cycle)


		# processing raw jobvar
		groups={}
		compstr_list=[]		# list of jobvars with composite_string type
		eval_list=[]		# list of jobvars with eval type
		raw_jobvar_content={}
		priority={}
		for jobvar_name, value in raw_jobvars.items():
			if 'type' not in value:
				raise JobvarListNotSetupError('Jobvar list type not setup: %s', jobvar_name)

			# register jobvar groups
			group=value.get('group','default')
			if group in groups:
				groups[group].append(jobvar_name)
			else:
				groups[group]=[jobvar_name]
			

			# register compstr/eval
			if value['type'] in ['composite_string','compositeString']:
				compstr_list.append(jobvar_name)
			if value['type'] in ['eval']:
				eval_list.append(jobvar_name)

			# set priority, which determines the order of which the value is resolved. effective as integers in [0,9]
			if 'priority' in value:
				priority[jobvar_name]=value['priority']
			else:
				priority[jobvar_name]=10 # won't resolve

			# put attributes in value to value['param']; to simplify user definition
			param=value.get('param',{})
			value_wo_param={k:v for k,v in value.items() if k!='param'}
			if 'param' not in value:
				value['param']={}
			value['param'].update(value_wo_param)

			raw_jobvar_content[jobvar_name] = {}
			raw_jobvar_content[jobvar_name]['instance'] = self.__ext_mgr.load_ext_common('jobvar', value)
			# name maps bridge jobvar_single (jobvar extension) and name_map (task profile)
			raw_jobvar_content[jobvar_name]['name_map'] = value.get('name_map', {'value':jobvar_name})


		#combining groups other than default
		overall_jobvar_list=[]
		for group in groups:
			if group == 'default':	#vars in default groups is not expanded
				continue

			# get jobvar list for this group
			cycle = 0
			varlist_in_group = []		# [jobvar_in_group for subjobs]
			while cycle < max_cycle:
				cycle += 1

				#extend varlist_in_group, using shortest length of all jobvars
				try:
					jobvars_in_group ={}		# {name:value for jobvars}
					for jobvar in groups[group]:
						content = raw_jobvar_content[jobvar]
						jobvar_single = content['instance'].next()
						jobvars_in_group.update(_jobvar_name_map(jobvar_single, content['name_map']))
					varlist_in_group.append(jobvars_in_group)
				except StopIteration:
					break

				#if only composite_string/eval jobvars in group, then cycle = 1
				all_jobvars_are_resolver = True
				for jobvar in groups[group]:
					if (jobvar not in (compstr_list+eval_list)):
						all_jobvars_are_resolver = False
				if all_jobvars_are_resolver:
					break
				

			# expand overall list with varlist in group
			expanded_list=[]
			if overall_jobvar_list == []:
				overall_jobvar_list = [{}]
			for new_jobvars in varlist_in_group:
				for orig_jobvars in overall_jobvar_list:
					if len(expanded_list)>=max_cycle:
						break
					expander=copy.deepcopy(orig_jobvars)
					expander.update(new_jobvars)
					expanded_list.append(expander)
			
			if len(expanded_list)>max_cycle:
				expanded_list=expanded_list[:max_cycle]	
			overall_jobvar_list=copy.deepcopy(expanded_list)

		# attach vars in default group
		cycle = 0
		varlist_default_group = []		# [jobvar_default_group for subjobs]
		while cycle < max_cycle:
			cycle += 1

			#extend varlist_default_group, using shortest length of all jobvars
			try:
				jobvars_default_group ={}		# {name:value for jobvars}
				for jobvar in groups['default']:
					content = raw_jobvar_content[jobvar]
					jobvar_single = content['instance'].next()
					jobvars_default_group.update(_jobvar_name_map(jobvar_single, content['name_map']))
				varlist_default_group.append(jobvars_default_group)
			except:
				break

		# combine varlist in default groups and in other groups
		if overall_jobvar_list == []:
			overall_jobvar_list = varlist_default_group
		elif varlist_default_group == []:
			pass
		else:
			shorter_len = len(overall_jobvar_list) if len(overall_jobvar_list)<len(varlist_default_group) else len(varlist_default_group)
			tmp_list=[]
			for i in range(shorter_len):
				j=copy.deepcopy(overall_jobvar_list[i])
				j.update(varlist_default_group[i])
				tmp_list.append(j)
		
			overall_jobvar_list=tmp_list

		# Resolving the values of composite_string and eval, from priority 10->0
		# replace $(var_name)/${var_name} with actual values in the subjob
		for i_subjob in range(len(overall_jobvar_list)):
			jobvars = copy.deepcopy(overall_jobvar_list[i_subjob])
			for jobvar in jobvars: #jobvar -> pythonic vars; (to do: avoiding conflict)
				code_str=str(jobvar)+"="+str(jobvars[jobvar])+""	#eval the python_var as a int
				code_str2=str(jobvar)+"='"+str(jobvars[jobvar])+"'"	#eval the python_var as a string
				try:
					exec(code_str)
				except:
					exec(code_str2)
			for p_now in range(0,11)[::-1]: 
				for jobvar0 in jobvars:
					if priority[jobvar0]==p_now:
						# try resolving composite string
						if jobvar0 in compstr_list:
							regex='\$\(([^)]+)'		# match $(jobvar)
							regex2='\$\{([^}]+)'	# match ${jobvar}
							while re.search(regex, str(jobvars[jobvar0])):
								match=re.search(regex, str(jobvars[jobvar0]))
								var_name=match.group(0)[2:]
								s=jobvars[jobvar0].replace('$('+var_name+')',str(jobvars[var_name]))
								jobvars[jobvar0]=s
#							while re.search(regex2, jobvars[jobvar0]):
#								match=re.search(regex2, jobvars[jobvar0])
#								var_name=match.group(0)[2:]
#								s=jobvars[jobvar0].replace('${'+var_name+'}',str(jobvars[var_name]))
#								jobvars[jobvar0]=s
							
						# try resolving eval
						if jobvar0 in eval_list:
							# bug: pythonic_jobvars in eval are treated as strings when they should be integers. how to fix?
							eval_result=eval(jobvars[jobvar0])
							jobvars[jobvar0]=eval_result

						# update pythonic var
						exec(str(jobvar0)+"='"+str(jobvars[jobvar0])+"'") 			
			overall_jobvar_list[i_subjob]=copy.deepcopy(jobvars)

		return overall_jobvar_list
