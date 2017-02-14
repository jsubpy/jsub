import datetime

from jsub.error import TaskIdFormatError

class Task(object):
    def __init__(self, data={}):
        self.data = data
        if 'created_at' not in self.data:
            self.data['created_at'] = datetime.datetime.utcnow().isoformat()

    def update_now(self):
        self.data['updated_at'] = datetime.datetime.utcnow().isoformat()


class TaskPool(object):
    def __init__(self, repo):
        self.__repo = repo

    def save(self, task):
        task.update_now()
        self.__repo.save_task(task.data)

    def create(self, task_data):
        task = Task(task_data)
        self.save(task)
        return task

    def all(self):
        tasks = []
        all_data = self.__repo.all_task_data()
        for data in all_data:
            tasks.append(Task(data))
        return tasks

    def find(self, task_id):
        if isinstance(task_id, int):
            data = self.__repo.find_by_id(task_id)
            return Task(data)

        tasks = []
        if isinstance(task_id, list):
            if not all(isinstance(t_id, int) for t_id in task_id):
                raise TaskIdFormatError('Not all task ids are type int: %s' % task_id)
            tasks_data = self.__repo.find_by_ids(task_id)
            for task_data in tasks_data:
                tasks.append(Task(task_data))
        return tasks
