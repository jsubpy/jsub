import os
import copy
import re

class Jobvar(object):
	def __init__(self, manager, task_id, sub_id, jobvar, max_cycle):
		self.__manager = manager
		self.__ext_mgr=self.__manager.load_ext_manager()
		self.__task = self.__manager.load_task(task_id)
		self.__sub_id = sub_id
		self.__jobvar = jobvar
		self.__max_cycle = max_cycle

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

		jobvar_data=self.__task.data.get('jobvar')
		print("Showing the info of subjob variables for task %s:"%str(self.__task.data['id']))

		mode=self.__task.data['scenario']['param']['splitter'].get('mode')
		if mode not in ['splitByJobvar', 'splitByJobvars']:
			print("Command invalid because splitter mode for the task is not splitByJobvars")
			return 0

		if (self.__sub_id is not None) and (self.__jobvar is None):
			#print the jobvar sets for the subjob
			try:
				jobvars_this_subjob = jobvar_data[self.__sub_id]
				print("The value of subjob variables for subjob %d are as following:"%int(self.__sub_id))
				for jobvar in jobvars_this_subjob:
					print("%s: %s"%(jobvar,jobvars_this_subjob[jobvar]))
			except:
				print("Can't get variables for subjob %d, bad index?"%int(self.__sub_id))

		if (self.__sub_id is None):
			if self.__jobvar is None: # print the list of jobvars
				try:
					jobvar_info=self.__task.data['scenario']['param']['splitter']['jobvarLists']
				except:
					jobvar_info=self.__task.data['scenario']['param']['splitter']['jobvar_lists']
				if jobvar_info is None:
					print('There is no info for any jobvar.')
				else:
					len_count=0
					var_count=0
					print("There're following jobvar lists:")
					for key in jobvar_info:
						print('%s'%key)
						var_count+=1
						len_count=len(jobvar_info[key])
					print("")		
					print("There're %s jobvar lists, each with a length of %s. You can use -i, -j parameters to check their values"%(var_count, len_count))
				
			else:
				try:
					jobvar_info=self.__task.data['scenario']['param']['splitter']['jobvarLists'].get(self.__jobvar)
				except:
					jobvar_info=self.__task.data['scenario']['param']['splitter']['jobvar_lists'].get(self.__jobvar)

				if jobvar_info is None:
					print('There is no info for jobvar %s.'%self.__jobvar)
				else:
					print("Parameters of jobvar list %s are as following:"%self.__jobvar)
					for key in jobvar_info:
						print('%s: %s'%(key, jobvar_info[key]))
					print("")		

					# put attributes in jobvar_info to jobvar_info['param']; to simplify user definition
					param=jobvar_info.get('param',{})
					jobvar_info_wo_param={k:v for k,v in jobvar_info.items() if k!='param'}
					if 'param' not in jobvar_info:
						jobvar_info['param']={}
					jobvar_info['param'].update(jobvar_info_wo_param)
					# loading jobvar and generate list
					print("Indexes and values for this jobvar list are:")
					jobvar_instance=self.__ext_mgr.load_ext_common('jobvar',jobvar_info)
					cycle=0
					cycle_end=False
					while cycle <self.__max_cycle:
						try:
							jobvar_single = jobvar_instance.next()
							print('%d: %s'%(cycle,str(jobvar_single['value'])))
						except StopIteration:
							cycle_end=True
							break
						cycle+=1
						# length=1 for eval/compstr
						if jobvar_info['type'] in ['eval','composite_string','compositeString']:
							cycle_end=True
							break
					if not cycle_end:
						print("...")
				
				
					
		return 0
