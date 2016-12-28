run_on = 'local'
run_on = 'remote'

run_on_background = True

# could be used for tests
run_on_foregroud = True

import os

class Local(object):
    def __init__(self, param):
        self.__work_dir = os.path.expanduser(param.get('work_dir'))

    def property(self):
        return {}

    def main_work_dir(self, task_id):
        return os.path.join(self.__work_dir, str(task_id), 'main')
