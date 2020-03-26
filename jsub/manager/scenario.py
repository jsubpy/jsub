from jsub.manager.error import ScenarioNotSetupError

class ScenarioManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def build(self, scenario_data, backend_property):
        if 'type' not in scenario_data:
            raise ScenarioNotSetupError('Must setup a scenario in task profile')
        scenario = self.__ext_mgr.load_ext_common('scenario', scenario_data)
        return scenario.build(backend_property)
