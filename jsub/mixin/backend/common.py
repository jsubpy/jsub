import os

class Common(object):
    def initialize_common_param(self):
        if 'work_dir' in self._param:
            self._work_dir = os.path.expanduser(self._param.get('work_dir'))
        else:
            self._work_dir = os.path.expanduser(self._param.get('default_work_dir'))

    def work_root(self, task_id):
        return os.path.join(self._work_dir, str(task_id))
