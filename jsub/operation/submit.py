import os
import logging

from jsub.util import safe_mkdir
from jsub.util import safe_rmdir

class Submit(object):
    def __init__(self, manager, task, sub_ids=None, dry_run=False):
        self.__manager = manager
        self.__task    = self.__manager.load_task(task)
        self.__sub_ids = sub_ids
        self.__dry_run = dry_run

        self.__logger = logging.getLogger('JSUB')

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
        self.__launcher_mgr  = self.__manager.load_launcher_manager()


    def handle(self):
        work_root = self.__backend_mgr.work_root(self.__task.data['backend'], self.__task.data['task_id'])

        main_root = os.path.join(work_root, 'main')

        safe_rmdir(main_root)
        safe_mkdir(main_root)

        self.__create_input(main_root)
        self.__create_scenario(main_root)
        self.__create_action(main_root)
        self.__create_navigator(main_root)
        self.__create_bootstrap(main_root)

        launcher_exe = self.__create_launcher(work_root)

        self.__submit(launcher_exe)


    def __create_input(self, main_root):
        content = self.__manager.load_content()
        content.get(self.__task.data['task_id'], 'input', os.path.join(main_root, 'input'))

    def __create_scenario(self, main_root):
        scenario_dir = os.path.join(main_root, 'scenario')
        safe_mkdir(scenario_dir)

        action_default = {}
        for unit, param in self.__task.data['workflow'].items():
            action_default[unit] = self.__action_mgr.default_config(param['type'])

        navigators = self.__config_mgr.navigator()
        scenario_format = self.__navigator_mgr.scenario_format(navigators)

        self.__scenario_mgr.create_scenario_file(self.__task.data, action_default, scenario_format, scenario_dir)

    def __create_action(self, main_root):
        action_dir = os.path.join(main_root, 'action')
        safe_mkdir(action_dir)

        actions = set()
        for unit, param in self.__task.data['workflow'].items():
            actions.add(param['type'])
        self.__action_mgr.create_actions(actions, action_dir)

    def __create_navigator(self, main_root):
        navigator_dir = os.path.join(main_root, 'navigator')
        safe_mkdir(navigator_dir)

        navigators = self.__config_mgr.navigator()
        self.__navigator_mgr.create_navigators(navigators, navigator_dir)

    def __create_bootstrap(self, main_root):
        bootstrap_dir = os.path.join(main_root, 'bootstrap')
        safe_mkdir(bootstrap_dir)

        bootstrap = self.__config_mgr.bootstrap()
        self.__bootstrap_mgr.create_bootstrap(bootstrap, bootstrap_dir)

    def __create_launcher(self, work_root):
        launcher = self.__task.data['backend']['param']['launcher']
        return self.__launcher_mgr.create_launcher(launcher, work_root)


    def __submit(self, launcher_exe):
        if self.__dry_run:
            return
        result = self.__backend_mgr.submit(self.__task.data['backend'], self.__task.data['task_id'], self.__sub_ids, launcher_exe)

        self.__logger.debug(result)
