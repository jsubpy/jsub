import click

from jsub import Jsub
import pprint

class Show(object):
    def __init__(self, jsubrc, task_id):
        self.__jsubrc = jsubrc
        self.__task_id = task_id

    def execute(self):
        click.echo('Showing the task data of task %d.'%self.__task_id)
        click.echo('')

        j = Jsub(self.__jsubrc)
        task_data = j.show(self.__task_id)
        task_report=pprint.pformat(task_data,depth=8)
        click.echo(task_report)
        click.echo('')
