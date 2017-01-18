import os

from jsub.util import safe_copy

class ActionManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def __action_param(self, action_type):
        action_param = self.__ext_mgr.ext_config('action', action_type, 'param')
        return action_param

    def __action_var(self, action_type):
        action_var = self.__ext_mgr.ext_config('action', action_type, 'action_var')
        return action_var

    def default_config(self, action_type):
        action_config = {}
        action_config['param'] = self.__action_param(action_type)
        action_config['actvar'] = self.__action_var(action_type)
        return action_config

    def create_actions(self, actions, dst_dir):
        for action_type in actions:
            action_dir = self.__ext_mgr.ext_dir('action', action_type)
            action_param = self.__action_param(action_dir)
            executable = action_param.get('executable', 'run')

            src_exe = os.path.join(action_dir, executable)
            dst_exe = os.path.join(dst_dir, action_type, executable)
            safe_copy(src_exe, dst_exe)
