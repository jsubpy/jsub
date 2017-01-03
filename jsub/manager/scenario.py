import os
import copy

class ScenarioManager(object):
    def __init__(self):
        pass

    def __action_param(self, action_output, action_input):
        for k, v in action_input.items():
            if k == 'pass_var':
                if k not in action_output:
                    action_output[k] = {}
                for var, method in v.items():
                    action_output[k][var] = method if isinstance(method, list) else [method]
            else:
                action_output[k] = copy.deepcopy(v)

    def create_scenario_file(self, task_data, action_default, dst_dir):
        scenario = {}

        scenario['workflow'] = {}
        for unit, param in task_data['workflow'].items():
            scenario['workflow'][unit] = {}

            dep = param.get('depend_on', [])
            if not isinstance(dep, list):
                dep = [dep]
            scenario['workflow'][unit]['depend_on'] = dep

            scenario['workflow'][unit]['action'] = {}
            self.__action_param(scenario['workflow'][unit]['action'], action_default[unit].get('action', {}))
            self.__action_param(scenario['workflow'][unit]['action'], param.get('action', {}))

            scenario['workflow'][unit]['actvar'] = copy.deepcopy(action_default[unit].get('actvar', {}))
            scenario['workflow'][unit]['actvar'].update(param.get('actvar', {}))

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

        scenario['event'] = task_data['event']

        scenario_file = os.path.join(dst_dir, 'scenario.py')
        with open(scenario_file, 'w') as f:
            f.write(str(scenario))
