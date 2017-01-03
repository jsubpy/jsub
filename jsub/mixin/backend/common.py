import sys
import os

from jsub.util import safe_copy
from jsub.util import safe_mkdir

from jsub.error import LauncherNotFoundError

class Common(object):
    def initialize_param(self):
        if 'work_dir' in self._param:
            self._work_dir = os.path.expanduser(self._param.get('work_dir'))
        else:
            self._work_dir = os.path.expanduser(self._param.get('default_work_dir'))

    def main_work_dir(self, task_id):
        return os.path.join(self._work_dir, str(task_id), 'main')

    def create_launcher(self, task_id):
        backend_file = sys.modules[self.__class__.__module__].__file__
        backend_dir = os.path.dirname(backend_file)
        launcher_path = os.path.join(backend_dir, 'launcher')

        if not os.path.isfile(launcher_path):
            raise LauncherNotFoundError('Launcher "%s" not found' % launcher_path)

        task_work_dir = os.path.join(self._work_dir, str(task_id))
        safe_mkdir(task_work_dir)

        safe_copy(launcher_path, task_work_dir)
