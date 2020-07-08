import click

from jsub import Jsub

class Getlog(object):
	def __init__(self, jsubrc, task_id, sub_id, path):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__sub_id = sub_id
		self.__path = path

	def execute(self):
		j = Jsub(self.__jsubrc)
		if not self.__sub_id:
			click.echo("No sub ID specified, can't fetch log files.") 
		else:
			click.echo("Fetching the log files of subjob %s to the path: %s"%(self.__sub_id,self.__path))
			j.getlog(self.__task_id, self.__sub_id, path=self.__path)
