import os

from jsub.manager import Manager

from jsub.operation.create import Create
from jsub.operation.submit import Submit

class Operation(object):
    def __init__(self, jsubrc):
        self.__manager = Manager(jsubrc)


    def create(self, task_profile):
        handler = Create(self.__manager, task_profile)
        return handler.handle()

    def submit(self, task, sub_ids=None, dry_run=False):
        handler = Submit(self.__manager, task, sub_ids, dry_run)
        return handler.handle()
