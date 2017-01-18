import os

from jsub.log               import add_stream_logger

from jsub.task              import TaskPool

from jsub.manager.config    import ConfigManager
from jsub.manager.extension import ExtensionManager

from jsub.manager.app       import AppManager
from jsub.manager.splitter  import SplitterManager
from jsub.manager.backend   import BackendManager
from jsub.manager.bootstrap import BootstrapManager
from jsub.manager.scenario  import ScenarioManager
from jsub.manager.navigator import NavigatorManager
from jsub.manager.action    import ActionManager
from jsub.manager.launcher  import LauncherManager

class Manager(object):
    def __init__(self, jsubrc, root_dir):
        self.__jsubrc     = os.path.expanduser(jsubrc)
        self.__root_dir   = root_dir

        self.__config_mgr = None
        self.__ext_mgr    = None

        self.__repo       = None
        self.__content    = None

        self.__task_pool  = None


    def init_logging(self):
        level = self.load_config_manager().setting('log_level')
        add_stream_logger(level)


    def load_config_manager(self):
        if self.__config_mgr is None:
            self.__config_mgr = ConfigManager(self.__jsubrc)
        return self.__config_mgr

    def load_ext_manager(self):
        if self.__ext_mgr is None:
            extensions = self.load_config_manager().extensions()
            self.__ext_mgr = ExtensionManager(extensions)
        return self.__ext_mgr


    def load_app_manager(self):
        return AppManager(self.load_ext_manager())

    def load_splitter_manager(self):
        return SplitterManager(self.load_ext_manager())

    def load_backend_manager(self):
        return BackendManager(self.load_ext_manager())

    def load_bootstrap_manager(self):
        return BootstrapManager(self.load_ext_manager())

    def load_scenario_manager(self):
        return ScenarioManager()

    def load_navigator_manager(self):
        return NavigatorManager(self.load_ext_manager())

    def load_action_manager(self):
        return ActionManager(self.load_ext_manager())

    def load_launcher_manager(self):
        return LauncherManager(self.load_ext_manager())


    def load_repo(self):
        if self.__repo is None:
            config_repo = self.load_config_manager().repo()
            self.__repo = self.load_ext_manager().load_ext_common('repo', config_repo)
        return self.__repo

    def load_content(self):
        if self.__content is None:
            config_content = self.load_config_manager().content()
            self.__content = self.load_ext_manager().load_ext_common('content', config_content)
        return self.__content


    def load_task_pool(self):
        if self.__task_pool is None:
            self.__task_pool = TaskPool(self.load_repo())
        return self.__task_pool

    def load_task(self, task):
        if isinstance(task, int):
            task_pool = self.load_task_pool()
            task_obj = task_pool.find(task)
        else:
            task_obj = task
        return task_obj
