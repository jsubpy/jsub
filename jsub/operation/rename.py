class Rename(object):
    def __init__(self, manager, task, new_name):
        self.__manager  = manager
        self.__task     = self.__manager.load_task(task)
        self.__new_name = new_name

    def handle(self):
        self.__task.data['name'] = self.__new_name
        task_pool = self.__manager.load_task_pool()
        task_pool.save(self.__task)
