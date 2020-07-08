# This command reschedules matched subjobs in a task
import click

from jsub import Jsub

class Reschedule(object):
	def __init__(self, jsubrc, task_id, status, sub_id, backend_id):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__status = status
		try:
			self.__sub_id = [int(x) for x in sub_id.split(',')]
		except:
			self.__sub_id = None
		try:
			self.__backend_id = [int(x) for x in backend_id.split(',')]
		except:
			self.__backend_id = None	

	def execute(self):
		j = Jsub(self.__jsubrc)
	
		j.reschedule(self.__task_id, self.__status, self.__sub_id, self.__backend_id)
