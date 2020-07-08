import os

class Common(object):
    def initialize_common_param(self):
        self._run_dir = os.path.expanduser(self._param.get('runDir'))

    def get_run_root(self, task_id):
        return os.path.join(self._run_dir, str(task_id))
