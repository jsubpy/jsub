import os

from jsub.operation import Operation


class Jsub(object):
    def __init__(self, jsubrc='~/.jsubrc'):
        self.__jsubrc = jsubrc
        self.__operation = None
        self.__root_dir = os.path.dirname(os.path.realpath(__file__))

    def __load_operation(self):
        if self.__operation is None:
            self.__operation = Operation(self.__jsubrc, self.__root_dir)
        return self.__operation


    def version(self):
        with open(os.path.join(self.__root_dir, 'VERSION'), 'r') as f:
            ver = f.read()
        return ver.strip()


    def create(self, task_profile):
        op = self.__load_operation()
        return op.create(task_profile)

    def submit(self, task, job_ids=None, dry_run=False):
        op = self.__load_operation()
        return op.submit(task, job_ids, dry_run)

    def list(self, task_id=None):
        op = self.__load_operation()
        return op.list(task_id)

    def show(self, task_id):
        op = self.__load_operation()
        return op.list(task_id)

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
