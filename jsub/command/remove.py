import click

from jsub import Jsub

class Remove(object):
	def __init__(self, jsubrc, task_id, force):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__force = force
	
	def execute(self):
		click.echo('Removing task %d'%self.__task_id)
		
		j = Jsub(self.__jsubrc)
		j.remove(self.__task_id, force = self.__force)
