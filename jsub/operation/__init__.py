class Operation(object):
    def __init__(self, manager):
        self.__manager = manager


    def rename(self, task, new_name):
        from jsub.operation.rename import Rename
        return Rename(self.__manager, task, new_name).handle()

    def create(self, task_profile):
        from jsub.operation.create import Create
        return Create(self.__manager, task_profile).handle()

    def submit(self, task, sub_ids=None, dry_run=False):
        from jsub.operation.submit import Submit
        return Submit(self.__manager, task, sub_ids, dry_run).handle()

    def ls(self, task_id):
        from jsub.operation.ls import Ls
        return Ls(self.__manager, task_id).handle()
