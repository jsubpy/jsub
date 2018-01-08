import click

from jsub import Jsub

class Rename(object):
    def __init__(self, config_user, task_id, new_name):
        self.__config_user = config_user
        self.__task_id = task_id
        self.__new_name = new_name

    def execute(self):
        click.echo('Rename...')

        j = Jsub(self.__config_user)
        j.rename(self.__task_id, self.__new_name)
