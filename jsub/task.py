import datetime

class Task:
    def __init__(self, task_id, repo):
        self.__repo = repo
        self.created_at = datetime.datetime.utcnow().isoformat()
        self.task_id = task_id
        self.metadata = {}

    def save(self):
        properties = {}
        properties['task_id'] = self.task_id
        properties['metadata'] = self.metadata
        properties['created_at'] = self.created_at
        properties['updated_at'] = datetime.datetime.utcnow().isoformat()
        self.__repo.save(**properties)


class TaskPool:
    def __init__(self, repo):
        self.__repo = repo

    def new():
        task_id = self.__repo.new_task_id()
        task = new Task(task_id, self.__repo)
        return task
