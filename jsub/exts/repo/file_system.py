import os
import json
import logging
import fcntl

from jsub.util  import safe_mkdir
from jsub.error import RepoReadError
from jsub.error import TaskNotFoundError

ID_FILENAME = 'id'

class FileSystem(object):
    def __init__(self, param):
        self.__repo_dir = os.path.expanduser(param.get('dir', '~/jsub/repo'))
        self.__task_dir = os.path.join(self.__repo_dir, 'task')
        self.__id_file  = os.path.join(self.__repo_dir, ID_FILENAME)

        self.__logger = logging.getLogger('JSUB')

        self.__create_repo_dir()

        self.__json_format = param.get('format', 'compact')

    def save_task(self, data):
        if 'id' not in data:
            data['id'] = self.__new_task_id()
        task_path = os.path.join(self.__task_dir, str(data['id']))

        data_str = self.__json_str(data)
        with open(task_path, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            f.truncate()
            f.write(data_str)

    def find_by_id(self, task_id):
        return self.task_data(task_id)

    def find_by_ids(self, task_ids):
        all_data = []
        for task_id in task_ids:
            try:
                td = self.task_data(task_id)
                all_data.append(td)
            except RepoReadError as e:
                self.__logger.debug(e)
        return all_data

    def all_task_data(self, order='asc'):
        task_ids = os.listdir(self.__task_dir)
        task_ids.sort(key=int, reverse=(order=='desc'))
        return self.find_by_ids(task_ids)

    def task_data(self, task_id):
        task_path = os.path.join(self.__task_dir, str(task_id))
        with open(task_path, 'a+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            data_str = f.read()

        try:
            return json.loads(data_str)
        except ValueError as e:
            raise RepoReadError('JSON decode error on task %s: %s' % (task_id, e))

    def __create_repo_dir(self):
        safe_mkdir(self.__repo_dir)
        safe_mkdir(self.__task_dir)

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
