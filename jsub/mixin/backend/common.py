import sys
import os
import shutil

from jsub.util import safe_copy
from jsub.util import safe_mkdir

from jsub.error import LauncherNotFoundError

class Common(object):
    def initialize_common_param(self):
        if 'work_dir' in self._param:
            self._work_dir = os.path.expanduser(self._param.get('work_dir'))
        else:
            self._work_dir = os.path.expanduser(self._param.get('default_work_dir'))

    def task_work_dir(self, task_id):
        return os.path.join(self._work_dir, str(task_id))

    def clean_work_dir(self, task_id):
        task_work_dir = self.task_work_dir(task_id)
        if os.path.isdir(task_work_dir):
            shutil.rmtree(task_work_dir)

    def main_work_dir(self, task_id):
        return os.path.join(self.task_work_dir(task_id), 'main')

    def launcher_path(self, task_id):
        backend_file = sys.modules[self.__class__.__module__].__file__
        backend_dir = os.path.dirname(backend_file)
        return os.path.join(backend_dir, 'launcher')

    def launcher_work_path(self, task_id):
        return os.path.join(self.task_work_dir(task_id), 'launcher')

    def launcher_log_dir(self, task_id):
        return os.path.join(self.task_work_dir(task_id), 'log')

    def create_launcher(self, task_id):
        launcher = self.launcher_path(task_id)

        if not os.path.isfile(launcher):
            raise LauncherNotFoundError('Launcher "%s" not found' % launcher)

        safe_copy(launcher, self.launcher_work_path(task_id))
