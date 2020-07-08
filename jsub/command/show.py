import click
import os
from jsub import Jsub
import pprint
import json
import yaml

class Show(object):
	def __init__(self, jsubrc, task_id, dump):
		self.__jsubrc = jsubrc
		self.__task_id = task_id
		self.__dump = dump

	def execute(self):
		click.echo('Showing the setup of task %d.'%self.__task_id)
		click.echo('')

		j = Jsub(self.__jsubrc)
		task_data = j.show(self.__task_id, self.__dump)
		task_data=task_data['scenario']['param']
		for key in task_data:
			if isinstance(task_data[key],dict):
				if 'param' in task_data[key]:
					task_data[key].update(task_data[key]['param'])
					task_data[key].pop('param',None)

		task_report=pprint.pformat(task_data,depth=None, indent=1)
		click.echo(task_report)
		click.echo('')

		if self.__dump:
			dump_path = os.path.realpath(self.__dump)
			with open(dump_path, 'w') as f:
				yaml.dump(task_data, f)
			click.echo('The above task profile is dumped to %s for modification.'%os.path.abspath(self.__dump))
