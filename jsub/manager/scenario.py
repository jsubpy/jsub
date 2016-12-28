import os

from jsub.util import dict_deep_update

class ScenarioManager(object):
    def __init__(self):
        pass

    def create_scenario_file(self, task_data, action_default, dst_dir):
        scenario = {}

        scenario['workflow'] = {}
        for unit, param in task_data['workflow'].items():
            scenario['workflow']['depend_on'] = param.get('depend_on', [])

            scenario['workflow']['action'] = action_default[unit].get('action', {})
            dict_deep_update(scenario['workflow']['action'], param.get('action', {}))

            scenario['workflow']['actvar'] = action_default[unit].get('actvar', {})
            dict_deep_update(scenario['workflow']['actvar'], param.get('actvar', {}))

        scenario['jobvar'] = {}
        sub_id = 0
        for jv in task_data['jobvar']:
            scenario['jobvar'][sub_id] = jv
            sub_id += 1

        scenario['general'] = {}
        scenario['general']['task_id']   = task_data['task_id']
        scenario['general']['app']       = task_data['app']
        scenario['general']['task_name'] = task_data['name']
        scenario['general']['backend']   = task_data['backend']['type']

        scenario_file = os.path.join(dst_dir, 'scenario.py')
        with open(scenario_file, 'w') as f:
            f.write(str(scenario))
