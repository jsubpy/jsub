import click

from jsub import Jsub

class Getlog(object):
	def __init__(self, jsubrc = None, task_id = None, sub_id = None, path = None, status = None, njobs = None):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__sub_id = sub_id
		self.__path = path
		self.__status = status
		self.__njobs = njobs

	def execute(self):
		j = Jsub(self.__jsubrc)
		click.echo("Fetching the log files of task %s"%(self.__task_id))
		if self.__sub_id:
			click.echo("Specifying sub IDs: %s"%(self.__sub_id))
		if self.__status:
			click.echo("Specifying job status: %s"%(self.__status))
		if (not self.__status) and (not self.__sub_id):
			click.echo("Cannot fetch log files. Please specify sub IDs or job status for the subjobs that you want to fetch log files.")
		else:
			j.getlog(self.__task_id, self.__sub_id, self.__status, self.__njobs, path=self.__path)	
