import os
import shutil

from jsub.util import safe_mkdir
from jsub.util import safe_copy

class Submit(object):
    def __init__(self, manager, task, dry_run=False):
        self.__manager = manager
        self.__task    = self.__manager.load_task(task)
        self.__dry_run = dry_run

        self.__initialize_manager()

    def __initialize_manager(self):
        self.__config_mgr    = self.__manager.load_config_manager()

        self.__backend_mgr   = self.__manager.load_backend_manager()
        self.__bootstrap_mgr = self.__manager.load_bootstrap_manager()
        self.__navigator_mgr = self.__manager.load_navigator_manager()
        self.__scenario_mgr  = self.__manager.load_scenario_manager()
        self.__action_mgr    = self.__manager.load_action_manager()


    def handle(self):
        main_work_dir = self.__backend_mgr.main_work_dir(self.__task.data['backend'], self.__task.data['task_id'])

        safe_mkdir(main_work_dir)

        self.__generate_bootstrap(main_work_dir)
        self.__generate_navigator(main_work_dir)
        self.__generate_scenario(main_work_dir)
        self.__generate_action(main_work_dir)
        self.__generate_input(main_work_dir)

        self.__submit()


    def __generate_bootstrap(self, main_work_dir):
        self.__bootstrap_mgr.create_bootstrap(main_work_dir)

    def __generate_navigator(self, main_work_dir):
        navigator_dir = os.path.join(main_work_dir, 'navigator')
        safe_mkdir(navigator_dir)
        navigators = self.__config_mgr.navigator()
        self.__navigator_mgr.create_navigators(navigators, navigator_dir)

    def __generate_scenario(self, main_work_dir):
        scenario_dir = os.path.join(main_work_dir, 'scenario')
        safe_mkdir(scenario_dir)

        action_default = {}
        for unit, param in self.__task.data['workflow'].items():
            action_type = param['action']['type']
            action_default[unit] = self.__action_mgr.default_param(action_type)

        self.__scenario_mgr.create_scenario_file(self.__task.data, action_default, scenario_dir)

    def __generate_action(self, main_work_dir):
        action_dir = os.path.join(main_work_dir, 'action')
        safe_mkdir(action_dir)
        actions = []
        for unit, param in self.__task.data['workflow'].items():
            actions.append(param['action']['type'])
        self.__action_mgr.create_actions(actions, action_dir)

    def __generate_input(self, main_work_dir):
        content = self.__manager.load_content()
        content.get(self.__task.data['task_id'], 'input', os.path.join(main_work_dir, 'input'))

    def __submit(self):
        if self.__dry_run:
            return
