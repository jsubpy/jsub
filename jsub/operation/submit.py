import os
import logging

from jsub.util import safe_mkdir

class Submit(object):
    def __init__(self, manager, task, sub_ids=None, dry_run=False):
        self.__manager = manager
        self.__task    = self.__manager.load_task(task)
        self.__sub_ids = sub_ids
        self.__dry_run = dry_run

        self.__logger  = logging.getLogger('JSUB')

        if self.__sub_ids is None:
            self.__sub_ids = list(range(len(self.__task.data['jobvar'])))

        self.__initialize_manager()

    def __initialize_manager(self):
        self.__config_mgr    = self.__manager.load_config_manager()

        self.__backend_mgr   = self.__manager.load_backend_manager()
        self.__bootstrap_mgr = self.__manager.load_bootstrap_manager()
        self.__navigator_mgr = self.__manager.load_navigator_manager()
        self.__scenario_mgr  = self.__manager.load_scenario_manager()
        self.__action_mgr    = self.__manager.load_action_manager()


    def handle(self):
        self.__backend_mgr.clean_work_dir(self.__task.data['backend'], self.__task.data['task_id'])

        main_work_dir = self.__backend_mgr.main_work_dir(self.__task.data['backend'], self.__task.data['task_id'])

        safe_mkdir(main_work_dir)

        self.__create_bootstrap(main_work_dir)
        self.__create_navigator(main_work_dir)
        self.__create_scenario(main_work_dir)
        self.__create_action(main_work_dir)
        self.__create_input(main_work_dir)

        self.__create_launcher()

        self.__submit()


    def __create_bootstrap(self, main_work_dir):
        bootstrap = self.__config_mgr.bootstrap()
        self.__bootstrap_mgr.create_bootstrap(bootstrap, main_work_dir)

    def __create_navigator(self, main_work_dir):
        navigator_dir = os.path.join(main_work_dir, 'navigator')
        safe_mkdir(navigator_dir)
        navigators = self.__config_mgr.navigator()
        self.__navigator_mgr.create_navigators(navigators, navigator_dir)

    def __create_scenario(self, main_work_dir):
        scenario_dir = os.path.join(main_work_dir, 'scenario')
        safe_mkdir(scenario_dir)

        action_default = {}
        for unit, param in self.__task.data['workflow'].items():
            action_type = param['action']['type']
            action_default[unit] = self.__action_mgr.default_param(action_type)

        self.__scenario_mgr.create_scenario_file(self.__task.data, action_default, scenario_dir)

    def __create_action(self, main_work_dir):
        action_dir = os.path.join(main_work_dir, 'action')
        safe_mkdir(action_dir)
        actions = []
        for unit, param in self.__task.data['workflow'].items():
            actions.append(param['action']['type'])
        self.__action_mgr.create_actions(actions, action_dir)

    def __create_input(self, main_work_dir):
        content = self.__manager.load_content()
        content.get(self.__task.data['task_id'], 'input', os.path.join(main_work_dir, 'input'))

    def __create_launcher(self):
        self.__backend_mgr.create_launcher(self.__task.data['backend'], self.__task.data['task_id'])

    def __submit(self):
        if self.__dry_run:
            return
        result = self.__backend_mgr.submit(self.__task.data['backend'], self.__task.data['task_id'], self.__sub_ids)

        self.__logger.debug(result)
