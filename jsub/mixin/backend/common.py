import os

class Common(object):
    def initialize_common_param(self):
        self._work_dir = os.path.expanduser(self._param.get('work_dir'))

    def get_work_root(self, task_id):
        return os.path.join(self._work_dir, str(task_id))
