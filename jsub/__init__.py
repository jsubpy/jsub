from jsub.operation import Operation

__version__ = '0.1.0'

def version():
    return __version__


def create(task_profile):
    op = Operation()
    return op.create(task_profile)


def submit(task_id, task_sub_id=[], dry_run=False):
    op = Operation()
    return op.submit(task_id=task_id, task_sub_id=task_sub_id, dry_run=dry_run)

def list(task_id=None):
    op = Operation()
    return op.list(task_id)

def show(task_id):
    op = Operation()
    return op.list(task_id)

def resubmit(task_id):
    op = Operation()
    return op.resubmit(task_id)

def reschedule(task_id):
    op = Operation()
    return op.reschedule(task_id)

def export(task_id, task_sub_id=[], output_dir='.', task_profile_format='yaml'):
    ''' Export job files (task_profile and input) for a task/job
        User can modify the files and submit again, with a special app
    '''
    op = Operation()
    return op.recreate(task_id=task_id, task_sub_id=task_sub_id, output_dir=output_dir, task_profile_format=task_profile_format)
