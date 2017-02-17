import click

from jsub import Jsub

class Rename(object):
    def __init__(self, jsubrc, task_id, new_name):
        self.__jsubrc = jsubrc
        self.__task_id = task_id
        self.__new_name = new_name

    def execute(self):
        click.echo('Rename...')

        j = Jsub(self.__jsubrc)
        j.rename(self.__task_id, self.__new_name)
