import os
import json
import fcntl

ID_FILENAME = 'id'

def _mkdir_p(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class FileSystem:
    def __init__(self, repo_dir='~/jsub_repo'):
        self.__repo_dir = os.path.expanduser(repo_dir)
        self.__task_dir = os.path.join(self.__repo_dir, 'task')
        self.__id_file = os.path.join(self.__repo_dir, ID_FILENAME)

        self.__create_repo_dir()

    def save_task(self, props):
        if 'task_id' not in props:
            props['task_id'] = self.__new_task_id()
        task_path = os.path.join(self.__task_dir, str(props['task_id']))
        with open(task_path, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            f.truncate()
            f.write(json.dumps(props))

    def all_task_props(self):
        all_props = []
        for task_id in os.listdir(self.__task_dir):
            all_props.append(self.task_props(task_id))
        return all_props

    def task_props(self, task_id):
        task_path = os.path.join(self.__task_dir, str(task_id))
        with open(task_path, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            props_str = f.read()
        return json.loads(props_str)

    def __create_repo_dir(self):
        _mkdir_p(self.__repo_dir)
        _mkdir_p(self.__task_dir)

    def __new_task_id(self):
        with open(self.__id_file, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            n = 0
            f.seek(0)
            n_read = f.read()
            if n_read:
                print(':::::::::: n_read: %s'%n_read)
                n = int(n_read)
            n += 1
            f.seek(0)
            f.truncate()
            f.write(str(n))
        return n
