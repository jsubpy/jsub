from jsub.config.config_loader import load_default
from jsub.application import app_load
from jsub.loader import Loader

class Manager:
    def __init__(self):
        self.__default_config = load_default()
        self.__loader = Loader(['jsub.exts'])

    def create(self, task_profile):
        print('manager create')
#        app = app_load(task_profile)
#        app.init()
#        app.split()
#        app.create_()
#        app.save(task_pool)
#        return 0

    def submit(self, task_id, job_id=None, dry_run=False):
        print('manager submit %s' % task_id)
#        task_pool.find(task_id)
#        backend.before_submit()
#        backend.submit()
#        backend.after_submit()
