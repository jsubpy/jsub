import click

from jsub import Jsub

class Show(object):
    def __init__(self, config_user, task_id):
        self.__config_user = config_user
        self.__task_id = task_id

    def execute(self):
        click.echo('Showing')

        j = Jsub(self.__config_user)
        j.show(self.__task_id)
