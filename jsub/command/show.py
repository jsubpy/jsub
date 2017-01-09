import click

from jsub import Jsub

class Show(object):
    def __init__(self, jsubrc, task_id):
        self.__jsubrc = jsubrc
        self.__task_id = task_id

    def execute(self):
        click.echo('Showing')

        j = Jsub(self.__jsubrc)
        j.show(self.__task_id)
