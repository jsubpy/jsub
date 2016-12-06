from jsub.manager import Manager

__version__ = '0.1.0'

def version():
    return __version__


def create(task_profile):
    manager = Manager()
    return manager.create(task_profile)


def submit(task_id, job_id=None, dry_run=False):
    manager = Manager()
    return manager.submit(task_id=task_id, job_id=job_id, dry_run=dry_run)

def list(task_id=None):
    manager = Manager()
    return manager.list(task_id)

def show(task_id):
    manager = Manager()
    return manager.list(task_id)

def resubmit(task_id):
    manager = Manager()
    return manager.resubmit(task_id)

def reschedule(task_id):
    manager = Manager()
    return manager.reschedule(task_id)
