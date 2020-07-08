# This command checks the backend running status of a task

import click

from jsub import Jsub
import datetime

class Status(object):
	def __init__(self, jsubrc, task_id,states, silent):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__states = states
		self.__silent = silent

	def execute(self):
		j = Jsub(self.__jsubrc)

		task_data = j.ls([self.__task_id])
		task_data = task_data[0]
		dst_time = datetime.datetime.strptime(task_data['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
		time_str = datetime.datetime.strftime(dst_time, '%Y-%m-%d %H:%M:%S')
		
		if not self.__silent:
			click.echo('Task ID: %s, Name: %s, Backend: %s, Created At: %s'%(task_data['id'],task_data['name'],task_data['backend']['type'],time_str))

		j.status(self.__task_id, self.__states,self.__silent)
