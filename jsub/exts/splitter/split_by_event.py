'''
input:
	- evtMax/evtMaxPerJob
	- totalEvents
	- maxSubjobs
	- njobs
	- jobvarsToSeq:
		varname: value
		varname2: value2
		...
	- jobvars:
		n: v

output:
	[{varname: value_0, varname2: value2_0 ..., n: v}, ...]
	
-number of subjobs decided by totalEvents/evtMax if attributes exist, or by njobs
'''
class SplitByEvent(object):
	def __init__(self, param):
		self.__ext_mgr = param['ext_mgr']
		self.__param = param
		self.__param.pop('ext_mgr')	#remove the unserializable object

	def split(self):
		evtmax = self.__param.get('evtMax',10)
		evtmax = self.__param.get('evtMaxPerJob',evtmax)
		index0 = self.__param.get('index0',0)
		totalEvents = self.__param.get('totalEvents')
		maxSubjobs = self.__param.get('maxSubjobs',100000)
		njobs = self.__param.get('njobs')
		jobvarsToSeq = self.__param.get('jobvarsToSeq',{})	#jobvars to add index
		jobvars = self.__param.get('jobvars',{})			#jobvars not to add index

		if njobs is None:	
			if totalEvents is not None:
				njobs = totalEvents/evtmax 
			else:
				njobs = 10	# default setting
		if njobs>maxSubjobs:
			njobs = maxSubjobs
		
		# expand jobvars to jobvar list: add suffix for strings; or add by idx for integers
		jobvar_list=[]
		for idx in range(njobs):
			idx_sum = idx + index0
			jobvar_set={}
			for key,value in jobvarsToSeq.items():
				try: 	#int	
					new_value=int(value)+idx_sum
				except:	#str
					new_value=str(value)+'_%s'%idx_sum

				jobvar_set.update({key:new_value})
			for key,value in jobvars.items():
				jobvar_set.update({key:value})
			jobvar_list.append(jobvar_set)
			
		return(jobvar_list)
