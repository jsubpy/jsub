import os
import logging

from jsub.config import dump_config_string

class Show(object):
	def __init__(self, manager, task_id):
		self.__manager = manager
		self.__task = self.__manager.load_task(task_id)
		self.__logger = logging.getLogger('JSUB')
	def handle(self):
		return(self.__task.data)
		
