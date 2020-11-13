from jsub.manager.error import ScenarioNotSetupError
import copy

class ScenarioManager(object):
	def __init__(self, ext_mgr):
		self.__ext_mgr = ext_mgr

	def build(self, scenario_data, backend_property):
		if 'type' not in scenario_data:
			raise ScenarioNotSetupError('Must setup a scenario in task profile')
		scenario = self.__ext_mgr.load_ext_common('scenario', scenario_data)
		
		result = scenario.build(backend_property)
		# check validity of action blocks in 
		popmarks=[]
		for unit, param in result['workflow'].items():
			try:
				if 'type' not in param or type(param) is not dict:
					popmarks.append(unit)
			except:
				popmarks.append(unit)
				
		for unit in popmarks:
			result['workflow'].pop(unit)
		# to put all attributes into actvars
		for unit, param in result['workflow'].items():
				actvar=param.get('actvar',{})
				oparam=copy.deepcopy(param)
				try:
					oparam.pop('actvar')
				except:
					pass
				actvar.update(oparam)
				result['workflow'][unit].update({'actvar':actvar})	


		return scenario.build(backend_property)
