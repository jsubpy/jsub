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

class ContextManager(object):
    def __init__(self):
        pass

    def create_context_file(self, task_data, action_default, context_format, dst_dir):
        context = {}

        context['workflow'] = {}
        for unit, data in task_data['workflow'].items():
            context['workflow'][unit] = {}

            # type
            context['workflow'][unit]['type'] = data['type']

            # depend_on
            dep = data.get('depend_on', [])
            if not isinstance(dep, list):
                dep = [dep]
            context['workflow'][unit]['depend_on'] = dep

            # param
            context['workflow'][unit]['param'] = {}
            _setup_action_param(context['workflow'][unit]['param'], action_default[unit].get('param', {}))
            _setup_action_param(context['workflow'][unit]['param'], data.get('param', {}))

            # actvar
            context['workflow'][unit]['actvar'] = copy.deepcopy(action_default[unit].get('actvar', {}))
            context['workflow'][unit]['actvar'].update(data.get('actvar', {}))

        context['jobvar'] = {}
        sub_id = 0
        for jv in task_data['jobvar']:
            context['jobvar'][str(sub_id)] = jv
            sub_id += 1

        context['general'] = {}
        context['general']['task_id']   = task_data['id']
        context['general']['scenario']       = task_data['scenario']['type']
        context['general']['task_name'] = task_data['name']
        context['general']['backend']   = task_data['backend']['type']
        context['general']['stop_after_unit_fail']   = True

        context['event'] = task_data['event']

        for fmt in context_format:
            context_file = os.path.join(dst_dir, 'context.'+fmt) 
            dump_config_file(context, context_file, fmt)
