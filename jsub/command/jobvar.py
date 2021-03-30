import click

from jsub import Jsub

from jsub.config import load_config_file

class Jobvar(object):
	def __init__(self, jsubrc, task_id, sub_id, jobvar, max_cycle):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__sub_id = sub_id
		self.__jobvar = jobvar
		self.__max_cycle = max_cycle

	def execute(self):
		click.echo("Showing the information of jobvar lists for task %d"%self.__task_id)
		click.echo("")

		j = Jsub(self.__jsubrc)
		j.jobvar(self.__task_id, sub_id = self.__sub_id, jobvar = self.__jobvar, max_cycle = self.__max_cycle)
