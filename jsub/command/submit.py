import click

from jsub import Jsub

class Submit(object):
    def __init__(self, jsubrc, task_id, dry_run):
        self.__jsubrc = jsubrc
        self.__task_id = task_id
        self.__dry_run = dry_run

    def execute(self):
        click.echo('Submitting')

        j = Jsub(self.__jsubrc)
        j.submit(self.__task_id, dry_run=self.__dry_run)
