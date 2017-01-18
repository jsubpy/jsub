import os
import copy

from jsub.config import dump_config_file

def _setup_action_param(action_output, action_input):
    for k, v in action_input.items():
        if k == 'pass_var':
            if k not in action_output:
                action_output[k] = {}
            for var, method in v.items():
                action_output[k][var] = method if isinstance(method, list) else [method]
        else:
            action_output[k] = copy.deepcopy(v)

class ScenarioManager(object):
    def __init__(self):
        pass

    def create_scenario_file(self, task_data, action_default, scenario_format, dst_dir):
        scenario = {}

        scenario['workflow'] = {}
        for unit, data in task_data['workflow'].items():
            scenario['workflow'][unit] = {}

            # type
            scenario['workflow'][unit]['type'] = data['type']

            # depend_on
            dep = data.get('depend_on', [])
            if not isinstance(dep, list):
                dep = [dep]
            scenario['workflow'][unit]['depend_on'] = dep

            # param
            scenario['workflow'][unit]['param'] = {}
            _setup_action_param(scenario['workflow'][unit]['param'], action_default[unit].get('param', {}))
            _setup_action_param(scenario['workflow'][unit]['param'], data.get('param', {}))

            # actvar
            scenario['workflow'][unit]['actvar'] = copy.deepcopy(action_default[unit].get('actvar', {}))
            scenario['workflow'][unit]['actvar'].update(data.get('actvar', {}))

        scenario['jobvar'] = {}
        sub_id = 0
        for jv in task_data['jobvar']:
            scenario['jobvar'][str(sub_id)] = jv
            sub_id += 1

        scenario['general'] = {}
        scenario['general']['task_id']   = task_data['task_id']
        scenario['general']['app']       = task_data['app']['type']
        scenario['general']['task_name'] = task_data['name']
        scenario['general']['backend']   = task_data['backend']['type']

        scenario['event'] = task_data['event']

        for fmt in scenario_format:
            scenario_file = os.path.join(dst_dir, 'scenario.'+fmt)
            dump_config_file(scenario, scenario_file, fmt)
