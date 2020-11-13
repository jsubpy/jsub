import os
import json
import logging
import fcntl

from jsub.util  import safe_mkdir
from jsub.util  import safe_rmdir
from jsub.error import RepoReadError
from jsub.error import TaskNotFoundError

ID_FILENAME = 'id'

class FileSystem(object):
	def __init__(self, param):
		self.__jsub_dir = os.path.expanduser(param.get('taskDir', '~/jsub/'))
#		self.__id_file  = os.path.join(self.__jsub_dir, ID_FILENAME)

		self.__logger = logging.getLogger('JSUB')

#		self.__create_repo_dir()

		self.__json_format = param.get('format', 'compact')

	def save_task(self, data):
		if 'id' not in data:
			safe_mkdir(self.__jsub_dir)
			data['id'] = self.__new_task_id()
		safe_mkdir(os.path.join(self.__jsub_dir,str(data['id']),'taskInfo'))
		task_path = os.path.join(self.__jsub_dir, str(data['id']),'taskInfo','repo')

		data_str = self.__json_str(data)
		with open(task_path, 'a+') as f:
			fcntl.flock(f, fcntl.LOCK_EX)
			f.seek(0)
			f.truncate()
			f.write(data_str)

	def delete_task(self, task_id):
		safe_rmdir(os.path.join(self.__jsub_dir,str(task_id)))

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
		task_ids =[d for d in os.listdir(self.__jsub_dir) if os.path.isdir(os.path.join(self.__jsub_dir,d))]
		task_ids.sort(key=int, reverse=(order=='desc'))
		return self.find_by_ids(task_ids)

	def task_data(self, task_id):
		safe_mkdir(os.path.join(self.__jsub_dir,str(task_id),'taskInfo'))
		task_path = os.path.join(self.__jsub_dir,str(task_id),'taskInfo','repo')
		with open(task_path, 'a+') as f:
			fcntl.flock(f, fcntl.LOCK_EX)
			f.seek(0)
			data_str = f.read()

		try:
			return json.loads(data_str)
		except ValueError as e:
			raise RepoReadError('JSON decode error on task %s: %s' % (task_id, e))

#	def __create_repo_dir(self):
#		safe_mkdir(self.__jsub_dir)

	def __new_task_id(self):
		task_ids =[int(d) for d in os.listdir(self.__jsub_dir) if os.path.isdir(os.path.join(self.__jsub_dir,d))]
		if not task_ids:
			return 1
		task_ids.sort(key=int, reverse=True)
		return(task_ids[0]+1)

	def __json_str(self, data):
		if self.__json_format == 'pretty':
			return json.dumps(data, indent=2)
		return json.dumps(data, separators=(',', ':'))
