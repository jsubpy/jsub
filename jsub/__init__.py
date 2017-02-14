import os

from jsub.manager   import Manager
from jsub.operation import Operation


JSUB_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


def version():
    with open(os.path.join(JSUB_ROOT_DIR, 'VERSION'), 'r') as f:
        ver = f.read()
    return ver.strip()


class Jsub(object):
    def __init__(self, jsubrc='~/.jsubrc'):
        self.__manager = Manager(jsubrc, JSUB_ROOT_DIR)
        self.__operation = None

        self.__manager.init_logging()


    def version(self):
        return self.__manager.version()


    def __load_operation(self):
        if self.__operation is None:
            self.__operation = Operation(self.__manager)
        return self.__operation


    def create(self, task_profile):
        op = self.__load_operation()
        return op.create(task_profile)

    def submit(self, task, sub_ids=None, dry_run=False):
        op = self.__load_operation()
        return op.submit(task, sub_ids, dry_run)

    def rename(self, task_id, new_task_name):
        op = self.__load_operation()
        return op.rename(task_id, new_task_name)

    def ls(self, task_id=None):
        op = self.__load_operation()
        return op.ls(task_id)

    def show(self, task_id):
        op = self.__load_operation()
        return op.show(task_id)

    def resubmit(self, task_id):
        op = self.__load_operation()
        return op.resubmit(task_id)

    def reschedule(self, task_id):
        op = self.__load_operation()
        return op.reschedule(task_id)

    def merge(self, task_id):
        op = self.__load_operation()
        return op.merge(task_id)

    def output(self, task_id):
        op = self.__load_operation()
        return op.output(task_id)

    def export(self, task_id, task_sub_id=[], output_dir='.', task_profile_format='yaml'):
        ''' Export job files (task_profile and input) for a task/job
            User can modify the files and submit again, with a common app
        '''
        op = self.__load_operation()
        return op.recreate(task_id=task_id, task_sub_id=task_sub_id, output_dir=output_dir, task_profile_format=task_profile_format)
