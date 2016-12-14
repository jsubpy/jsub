import os
import json
import fcntl

ID_FILENAME = 'id'

def _mkdir_p(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

class FileSystem(object):
    def __init__(self, param):
        self.__repo_dir = os.path.expanduser(param.get('dir', '~/jsub_repo'))
        self.__task_dir = os.path.join(self.__repo_dir, 'task')
        self.__id_file = os.path.join(self.__repo_dir, ID_FILENAME)

        self.__create_repo_dir()

        self.__json_format = param.get('format', 'compact')

    def save_task(self, data):
        if 'task_id' not in data:
            data['task_id'] = self.__new_task_id()
        task_path = os.path.join(self.__task_dir, str(data['task_id']))

        data_str = self.__json_str(data)
        with open(task_path, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            f.truncate()
            f.write(data_str)

    def all_task_data(self):
        all_data = []
        for task_id in os.listdir(self.__task_dir):
            all_data.append(self.task_data(task_id))
        return all_data

    def task_data(self, task_id):
        task_path = os.path.join(self.__task_dir, str(task_id))
        with open(task_path, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            data_str = f.read()
        return json.loads(data_str)

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
                n = int(n_read)
            n += 1
            f.seek(0)
            f.truncate()
            f.write(str(n))
        return n

    def __json_str(self, data):
        if self.__json_format == 'pretty':
            return json.dumps(data, indent=2)
        return json.dumps(data, separators=(',', ':'))
