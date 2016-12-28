import os

from jsub.util import safe_copy

from jsub.config import load_config_file

class ActionManager(object):
    def __init__(self, ext_mgr):
        self.__ext_mgr = ext_mgr

    def __action_config(self, action_dir):
        action_config_file = os.path.join(action_dir, 'config.yml')
        action_config = load_config_file(action_config_file)
        if 'action' not in action_config:
            action_config['action'] = {}
        if 'actvar' not in action_config:
            action_config['actvar'] = {}
        return action_config

    def default_param(self, action_type):
        action_dir = self.__ext_mgr.ext_dir('action', action_type)
        return self.__action_config(action_dir)

    def create_actions(self, actions, dst_dir):
        for action in actions:
            action_dir = self.__ext_mgr.ext_dir('action', action)
            action_config = self.__action_config(action_dir)

            executable = action_config['action'].get('executable', 'run')
            src_exe = os.path.join(action_dir, executable)
            dst_exe = os.path.join(dst_dir, action, executable)
            safe_copy(src_exe, dst_exe)
