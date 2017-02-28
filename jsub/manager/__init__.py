import os

from jsub.log  import add_stream_logger
from jsub.util import ensure_list


class Manager(object):
    def __init__(self, jsubrc, root_dir):
        self.__jsubrc     = os.path.expanduser(jsubrc)
        self.__root_dir   = root_dir

        self.__schema_mgr = None
        self.__config_mgr = None
        self.__pkg_mgr    = None
        self.__ext_mgr    = None

        self.__repo       = None
        self.__content    = None

        self.__task_pool  = None


    def init_logging(self):
        level = self.load_config_manager().config('log_level')
        add_stream_logger(level)

    def init_config(self):
        self.load_config_manager()
        self.load_pkg_manager()
        packages_config = self.__pkg_mgr.packages_config()
        self.__config_mgr.merge_packages_config(packages_config)


    def load_schema_manager(self):
        if self.__schema_mgr is None:
            from jsub.manager.schemaconfig import SchemaManager
            self.__schema_mgr = SchemaManager()
        return self.__schema_mgr

    def load_config_manager(self):
        if self.__config_mgr is None:
            from jsub.manager.config import ConfigManager
            self.__config_mgr = ConfigManager(self.load_schema_manager(), self.__jsubrc)
        return self.__config_mgr

    def load_pkg_manager(self):
        if self.__pkg_mgr is None:
            from jsub.manager.package import PackageManager
            packages = self.load_config_manager().config_jsubrc('package')
            packages = ensure_list(packages)
            self.__pkg_mgr = PackageManager(self.load_schema_manager(), packages)
        return self.__pkg_mgr

    def load_ext_manager(self):
        if self.__ext_mgr is None:
            from jsub.manager.extension import ExtensionManager
            packages = self.load_pkg_manager().packages()
            self.__ext_mgr = ExtensionManager(packages)
        return self.__ext_mgr


    def load_app_manager(self):
        from jsub.manager.app import AppManager
        return AppManager(self.load_ext_manager())

    def load_splitter_manager(self):
        from jsub.manager.splitter import SplitterManager
        return SplitterManager(self.load_ext_manager())

    def load_backend_manager(self):
        from jsub.manager.backend import BackendManager
        return BackendManager(self.load_ext_manager())

    def load_bootstrap_manager(self):
        from jsub.manager.bootstrap import BootstrapManager
        return BootstrapManager(self.load_ext_manager())

    def load_scenario_manager(self):
        from jsub.manager.scenario import ScenarioManager
        return ScenarioManager()

    def load_navigator_manager(self):
        from jsub.manager.navigator import NavigatorManager
        return NavigatorManager(self.load_ext_manager())

    def load_action_manager(self):
        from jsub.manager.action import ActionManager
        return ActionManager(self.load_ext_manager())

    def load_launcher_manager(self):
        from jsub.manager.launcher import LauncherManager
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
            from jsub.task import TaskPool
            self.__task_pool = TaskPool(self.load_repo())
        return self.__task_pool

    def load_task(self, task):
        if isinstance(task, int):
            task_pool = self.load_task_pool()
            task_obj = task_pool.find(task)
        else:
            task_obj = task
        return task_obj
