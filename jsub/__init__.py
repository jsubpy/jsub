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
        self.__manager = Manager(jsubrc)
        self.__operation = None


    def package(self):
        return self.__manager.load_pkg_manager().packages()

    def config(self):
        return self.__manager.load_config_manager().config()


    def __load_operation(self):
        if self.__operation is None:
            self.__operation = Operation(self.__manager)
        return self.__operation


    def rename(self, task, new_name):
        op = self.__load_operation()
        return op.rename(task, new_name)

    def create(self, task_profile):
        op = self.__load_operation()
        return op.create(task_profile)

    def submit(self, task, sub_ids=None, dry_run=False):
        op = self.__load_operation()
        return op.submit(task, sub_ids, dry_run)

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
